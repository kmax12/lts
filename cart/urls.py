from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template
from lifetime.models import Product
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    #cart stuff
    url(r'^add/$', 'cart.views.add_to_cart', name="add to cart"),
    url(r'^remove/$', 'cart.views.remove_from_cart', name="remove from cart"),
    url(r'^checkout/$', 'cart.views.checkout', name="checkout"),
    url(r'^confirm-checkout/$', 'cart.views.confirm_checkout', name="checkout"),
    url(r'^$', 'cart.views.view_cart', name="view_cart"),
)
