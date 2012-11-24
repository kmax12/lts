from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    url = models.URLField("Website", blank=True)
    company = models.CharField(max_length=50, blank=True)

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    img = models.CharField(max_length=100)
    price = models.FloatField()
    
    def __unicode__(self):
        return u'%s' % (self.name)

class Subscription(models.Model):
	product = models.ForeignKey(Product)
	user = models.ForeignKey(User)
	creation_date = models.DateTimeField(default=datetime.now, verbose_name='creation date') #date created
	length_days = models.IntegerField(default=0) #length of subscription in days
	total_quantity = models.IntegerField(default=0) # number of product per per year

class Order (models.Model):
	subscription = models.ForeignKey(Subscription)
	date_placed = models.DateTimeField(default=datetime.now, verbose_name='date placed') #date placed
	date_shipped =  models.DateTimeField(blank=True, null=True)
	shipped = models.BooleanField(default=False)
	item_quanity = models.IntegerField(default=0) # number of items in shipment


