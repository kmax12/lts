from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    img = models.CharField(max_length=100)
    price = models.FloatField()
    

    def __unicode__(self):
        return u'%s' % (self.name)
