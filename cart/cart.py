#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import models
from django.contrib.auth.models import User, AnonymousUser
CART_ID = 'CART-ID'


class ItemDoesNotExist(Exception):
    pass


class Cart:
    def __init__(self, request):
        self.associate_cart(request)

    def __iter__(self):
        for item in self.cart.item_set.all():
            yield item

    def new(self, request):      
        cart = models.Cart(creation_date=datetime.datetime.now())
        if isinstance(request.user, User):
            cart.user = request.user

        cart.save()

        request.session[CART_ID] = cart.id
        
        return cart

    def add(self, supply, unit_price, quantity=1):
        try:
            item = models.Item.objects.get(
                cart=self.cart,
                product=supply,
            )
        #add item to cart since it does not exist
        except models.Item.DoesNotExist:
            item = models.Item()
            item.cart = self.cart
            item.product = supply
            item.unit_price = unit_price
            item.quantity = quantity
            item.save()

    def remove(self, item):
        try:
            item = models.Item.objects.filter(cart=self.cart, object_id=item.id).delete()
        except models.Item.DoesNotExist:
            raise ItemDoesNotExist

    def get_supplies(self):
        supplies = [item.product for item in self.cart.item_set.all()] #problematic if lots of items in cart!!!
        return supplies


    def update(self, supply, quantity, unit_price=None):
        try:
            item = models.Item.objects.get(
                cart=self.cart,
                product=supply,
            )
        except models.Item.DoesNotExist:
            raise ItemDoesNotExist

    def associate_cart(self, request):
        cart_id = request.session.get(CART_ID)
        if cart_id:
            try:
                cart = models.Cart.objects.select_related().get(id=cart_id, checked_out=False)
                if cart.owner == None and isinstance(request.user, User):
                    cart.owner = request.user
            except:
                cart = self.new(request)
        else:
            cart = self.new(request)

        self.cart = cart

    def set_gift(self,gift=False):
        print gift
        self.cart.gift = gift
        self.cart.save()

    def clear(self):
        for item in self.cart.item_set.all():
            item.delete()

    def total(self):
        total = 0
        for item in self.cart.item_set.all():
            total += item.total_price

        return total

    def num_items(self):
        return self.cart.item_set.count()

    def is_gift(self):
        return self.cart.gift


    def checkout(self):
        try:
            self.cart.checked_out = True
            self.cart.save()
            return True
        except:
            return False
