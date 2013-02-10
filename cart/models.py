#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User
from django import forms

class Cart(models.Model):
    owner = models.ForeignKey(User, related_name='cart', blank=True, null=True)
    gift = models.BooleanField(verbose_name=_('cart is gift'), \
                                      default=False)
    creation_date = models.DateTimeField(verbose_name=_('creation date'))
    checked_out = models.BooleanField(verbose_name=_('checked out'),
                                      default=False)

    name = models.CharField(max_length=100)
    email =  models.EmailField(null=True)
    stripe_token = models.CharField(max_length=100)


    class Meta:
        verbose_name = _('Cart')
        verbose_name_plural = _('Carts')
        ordering = ('-creation_date',)

    def __unicode__(self):
        return unicode(self.creation_date)


class ItemManager(models.Manager):
    def get(self, *args, **kwargs):
        if 'product' in kwargs:
            kwargs['content_type'] = ContentType.objects.get_for_model( \
                                      type(kwargs['product'])
                                     )
            kwargs['object_id'] = kwargs['product'].pk
            del(kwargs['product'])
        return super(ItemManager, self).get(*args, **kwargs)


class Item(models.Model):
    cart = models.ForeignKey(Cart, verbose_name=_('cart'))
    quantity = models.PositiveIntegerField(verbose_name=_('quantity'))
    unit_price = models.DecimalField(verbose_name=_('unit price'), \
                                      max_digits=18, decimal_places=2
                                    )
    # product as generic relation
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()

    objects = ItemManager()

    class Meta:
        verbose_name = _('item')
        verbose_name_plural = _('items')
        ordering = ('cart',)

    def __unicode__(self):
        return 'Item in cart: ' + unicode(self.cart)

    def total_price(self):
        return self.quantity * self.unit_price
    total_price = property(total_price)

    # product
    def get_product(self):
        return self.content_type.get_object_for_this_type(id=self.object_id)

    def set_product(self, product):
        self.content_type = ContentType.objects.get_for_model(type(product))
        self.object_id = product.pk

    product = property(get_product, set_product)

class CheckoutForm(forms.Form):
    name = forms.CharField(label='Your Name', max_length=100)
    email = forms.EmailField(label='Your Email')
    tos = forms.BooleanField(label="<label for='id_tos'>Signing up signifies that you’ve read and agree to our <a href='/terms/'>Terms of Use</a> and <a href='/privacy/'>Privacy Policy</a>.</label>")

    def __init__(self, *args, **kwargs):
        super(CheckoutForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
                field = self.fields.get(field_name)  
                if field:
                    if type(field.widget) in (forms.TextInput, forms.DateInput):
                        field.widget = forms.TextInput(attrs={'placeholder': field.label})    

class CheckoutStudent(CheckoutForm):
    student = forms.CharField(widget=forms.HiddenInput(), initial="1")
    student_email = forms.EmailField(label='Student\'s Email')

class CheckoutSelf(CheckoutForm):
    student = forms.CharField(widget=forms.HiddenInput(), initial="0")
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

class ClaimGift(CheckoutForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
        
    
