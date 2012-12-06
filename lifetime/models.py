from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    prefered_card = models.CharField(default="", max_length=100)

    def get_orders(self):
        from utils.models import Order
        return Order.objects.select_related().filter(subscription__user = self.user) .order_by('-date_placed')

    def get_subscriptions(self):
        from utils.models import Subscription
        return Subscription.objects.select_related().filter(user = self.user)

    def get_cards(self):
        from utils.models import Card
        return Card.objects.select_related().filter(user = self.user)


User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

User.products = property(lambda u: Product.objects.filter(subscription__user=u))

User.address = property(lambda u: get_address(u))

def get_address(u):
    from utils.models import Address
    return Address.objects.get_or_create(user=u)[0]

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    img = models.CharField(max_length=100)
    price = models.FloatField()
    
    def __unicode__(self):
        return u'%s' % (self.name)