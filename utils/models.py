from django.db import models
from django.contrib.auth.models import User
from lifetime.models import Product

from datetime import datetime

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
