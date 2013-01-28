from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
import random, string


class Category(models.Model):
    name = models.CharField(max_length=100)

class Supply(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    categories = models.ManyToManyField(Category)

class Subscription(models.Model):
    owner = models.ForeignKey(User)
    supply = models.ForeignKey(Supply, related_name="subscription")
    creation_date = models.DateTimeField(default=datetime.now, verbose_name='creation date') #date created
    length_days = models.IntegerField(default=0) #length of Supply in days

    def last_order(self):
        order = Order.objects.filter(Subscription=self).latest('date_placed')
        if order:
            return order.date_placed
        return None

    def __unicode__(self):
        return self.owner.first_name + "," + self.product.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    img = models.CharField(max_length=100)
    price = models.FloatField()
    active = models.BooleanField(default=False)
    categories = models.ManyToManyField(Category)

    # units_per_shipment = models.IntegerField(default=0) #length of Supply in days
    # units_per_week = models.IntegerField(default=0) #length of Supply in days
    # units_per_year = models.IntegerField(default=0) #length of Supply in days
    # unit_name =models.CharField(max_length=100, default="units")

    
    def __unicode__(self):
        return u'%s' % (self.name)

class ProductDetail(models.Model):
    product = models.ForeignKey(Product)
    text = models.TextField()
    
    def __unicode__(self):
        return u'%s' % (self.text)

def promotion_code_generate():
    chars=string.ascii_uppercase+string.digits+string.ascii_lowercase
    while 1:
        prom_code = ''.join(random.choice(chars) for x in range(8))
        try:
            GiftModel.objects.get(code=prom_code)
        except:
            return prom_code

class Gift(models.Model):
    supply = models.ForeignKey(Supply, blank=True, null=True)
    code = models.CharField(default=promotion_code_generate, unique=True, max_length=8)

    def last_order(self):
        pass

    def claim(self, user):
        s = Supply(user=user, product=self.product)

class Order (models.Model):
    supply = models.ForeignKey(Supply)
    date_placed = models.DateTimeField(default=datetime.now, verbose_name='date placed') #date placed
    date_shipped =  models.DateTimeField(blank=True, null=True)
    item_quanity = models.IntegerField(default=0) # number of items in shipment

    def __unicode__(self):
        return self.Supply.product.name

    class Meta:
        get_latest_by = "date_placed"