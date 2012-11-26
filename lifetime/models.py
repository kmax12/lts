from django.db import models
from django.contrib.auth.models import User
# from utils.models import Card
from datetime import datetime

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    # prefered_card = models.ForeignKey(Card, blank=True, null=True, on_delete=models.SET_NULL)


User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    img = models.CharField(max_length=100)
    price = models.FloatField()
    
    def __unicode__(self):
        return u'%s' % (self.name)