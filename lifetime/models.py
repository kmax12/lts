from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
import random, string


class Category(models.Model):
    name = models.CharField(max_length=100)
    url_slug = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return self.name

class Supply(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    categories = models.ManyToManyField(Category)
    brands_text = models.CharField(max_length=100)
    photo = models.CharField(max_length=100)
    description = models.TextField(default="This is a description")
    url_slug = models.CharField(max_length=100, unique=True)

    def category_names(self):
        return map(str, self.categories.all())

    def __unicode__(self):
        return "%s | Cats: %s"%(self.name, ", ".join(self.category_names()))

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
        return self.owner.first_name + "," + self.supply.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default="This is a description")
    active = models.BooleanField(default=False)
    categories = models.ManyToManyField(Category)

    # price = models.FloatField()
    # units_per_shipment = models.IntegerField(default=0) #length of Supply in days
    # units_per_week = models.IntegerField(default=0) #length of Supply in days
    # units_per_year = models.IntegerField(default=0) #length of Supply in days
    # unit_name =models.CharField(max_length=100, default="units")

    def similar_categories(self, user=None):
        if not user:
            return self.categories.all()

        return self.categories.all().filter(pk__in = user.profile.get_categories())

    def similar_products(self, user=None):
        return Product.objects.filter(
            categories__in = self.similar_categories(user)
        )
    
    def __unicode__(self):
        return u'%s | %s' % (self.name, ", ".join([str(x) for x in self.categories.all()]))

class ProductImage(models.Model):
    product = models.ForeignKey(Product)
    image = models.TextField()
    
    def __unicode__(self):
        return u'%s' % (self.image)


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
    user = models.ForeignKey(User)
    product = models.ForeignKey(Product)
    date_placed = models.DateTimeField(default=datetime.now, verbose_name='date placed') #date placed
    date_shipped =  models.DateTimeField(blank=True, null=True)
    item_quanity = models.IntegerField(default=0) # number of items in shipment

    def __unicode__(self):
        return self.product.name

    class Meta:
        get_latest_by = "date_placed"