from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
import random, string
from datetime import datetime

class Subscription(models.Model):
    from lifetime.models import Product
    product = models.ForeignKey(Product)
    user = models.ForeignKey(User)
    creation_date = models.DateTimeField(default=datetime.now, verbose_name='creation date') #date created
    length_days = models.IntegerField(default=0) #length of subscription in days
    total_quantity = models.IntegerField(default=0) # number of product per per year

    def last_order(self):
        order = Order.objects.filter(subscription=self).latest('date_placed')
        if order:
            return order.date_placed

        return None


class Order (models.Model):
    subscription = models.ForeignKey(Subscription)
    date_placed = models.DateTimeField(default=datetime.now, verbose_name='date placed') #date placed
    date_shipped =  models.DateTimeField(blank=True, null=True)
    shipped = models.BooleanField(default=False)
    item_quanity = models.IntegerField(default=0) # number of items in shipment

class Card(models.Model):
    user = models.ForeignKey(User)
    token = models.TextField(max_length=50, default='')
    stripe_id = models.TextField(max_length=50, default='')
    card_type = models.TextField(max_length=50, default='')
    last4 = models.IntegerField(default=0)

def promotion_code_generate():
    chars=string.ascii_uppercase+string.digits+string.ascii_lowercase
    while 1:
        prom_code = ''.join(random.choice(chars) for x in range(8))
        try:
            GiftModel.objects.get(code=prom_code)
        except:
            return prom_code

class GiftModel(Subscription):
    subscription = models.ForeignKey(Subscription, blank=True, null=True, related_name="gift")
    code = models.CharField(default=promotion_code_generate, unique=True, max_length=8)

    def last_order(self):
        pass

    def claim(self, user):
        s = Subscription(user=user, product=self.product)

class Address(models.Model):
    """Model to store addresses for accounts"""
    user = models.ForeignKey(User, blank=True, null=True, unique=True)

    address_line1 = models.CharField("Address line 1", max_length = 45)
    address_line2 = models.CharField("Address line 2", max_length = 45, blank = True)
    city = models.CharField(max_length = 50, blank = False)
    state_province = models.CharField("State/Province", max_length = 40, blank = True)
    postal_code = models.CharField("Postal Code", max_length = 10)
    country = models.CharField("Country", default = "USA", max_length = 40, blank = True)

    creation_date = models.DateTimeField(default=datetime.now, verbose_name='creation date') #date created
    edited = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s <br> %s, %s" % (self.address_line1, self.city, self.state_province)

    class Meta:
        verbose_name_plural = "Addresses"
        unique_together = ("address_line1", "address_line2", "postal_code",
                           "city", "state_province", "country")


class AddressForm(ModelForm):
    class Meta:
        model = Address
        exclude = ('country', 'creation_date', 'user', 'edited')

