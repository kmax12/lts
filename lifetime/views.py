from django.views.generic.simple import direct_to_template
# from utils import cart
from cart import Cart
from utils.SubscriptionManager import SubscriptionManager
from lifetime.models import *
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt 
from django.db.models import F
import json


def home(request):
    template_values = {
        "title": "Lifetime Supply",
        "home_active" : "active",
        "products": Product.objects.all(),
    }

    return direct_to_template(request, 'home.html',
                             template_values)

def view_product(request, product):
    product = Product.objects.get(id=product) 

    template_values = {
        "title": product.name + " | Lifetime Supply",
        "product" : product
    }

    return direct_to_template(request, 'product_page.html',
                             template_values)








