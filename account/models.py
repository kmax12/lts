from django.db import models
from django.contrib.auth.models import User
from lifetime.models import *
from account.models import *
from datetime import datetime
from django.forms import ModelForm


# Create your models here.
class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    prefered_card = models.CharField(default="", max_length=100)

    def get_orders(self):
        return Order.objects.select_related().filter(user = self.user).order_by('-date_placed')

    def get_subscriptions(self):
        return Subscription.objects.select_related().filter(owner=self.user)

    def get_cards(self):
        return Card.objects.select_related().filter(owner = self.user)


User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

User.products = property(lambda u: Product.objects.filter(subscription__owner=u))

User.address = property(lambda u: Address.objects.get_or_create(owner=u)[0])

class Card(models.Model):
    owner = models.ForeignKey(User)
    token = models.TextField(max_length=50, default='')
    stripe_id = models.TextField(max_length=50, default='')
    card_type = models.TextField(max_length=50, default='')
    last4 = models.IntegerField(default=0)


class Address(models.Model):
    """Model to store addresses for accounts"""
    owner = models.ForeignKey(User, blank=True, null=True, unique=True)

    address_line1 = models.CharField("Address line 1", max_length = 45)
    address_line2 = models.CharField("Address line 2", max_length = 45, blank = True)
    city = models.CharField(max_length = 50, blank = False)
    state_province = models.CharField("State/Province", max_length = 40, blank = True)
    postal_code = models.CharField("Postal Code", max_length = 10)
    country = models.CharField("Country", default = "USA", max_length = 40, blank = True)

    creation_date = models.DateTimeField(default=datetime.now, verbose_name='creation date') #date created
    edited = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s \ %s \ %s, %s \%s" % (self.address_line1, self.address_line2, self.city, self.state_province, postal_code)

    class Meta:
        verbose_name_plural = "Addresses"
        unique_together = ("address_line1", "address_line2", "postal_code",
                           "city", "state_province", "country")


class AddressForm(ModelForm):
    class Meta:
        model = Address
        exclude = ('country', 'creation_date', 'owner', 'edited')