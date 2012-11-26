from django.db import models
from django.forms import ModelForm
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

class Address(models.Model):
    """Model to store addresses for accounts"""
    user = models.ForeignKey(User, blank=True, null=True)


    address_line1 = models.CharField("Address line 1", max_length = 45)
    address_line2 = models.CharField("Address line 2", max_length = 45, blank = True)
    postal_code = models.CharField("Postal Code", max_length = 10)
    city = models.CharField(max_length = 50, blank = False)
    state_province = models.CharField("State/Province", max_length = 40, blank = True)
    country = models.CharField("Country", default = "USA", max_length = 40, blank = True)

    creation_date = models.DateTimeField(default=datetime.now, verbose_name='creation date') #date created


    def __unicode__(self):
        return "%s, %s %s" % (self.city, self.state_province,
                              self.country)

    class Meta:
        verbose_name_plural = "Addresses"
        unique_together = ("address_line1", "address_line2", "postal_code",
                           "city", "state_province", "country")


class AddressForm(ModelForm):
    class Meta:
        model = Address
        exclude = ('country', 'creation_date', 'user')

