from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True) 
    stripe_id = models.TextField(max_length=50, default='')

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    img = models.CharField(max_length=100)
    price = models.FloatField()
    
    def __unicode__(self):
        return u'%s' % (self.name)