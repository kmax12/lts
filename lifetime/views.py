from django.views.generic.simple import direct_to_template
# from utils import cart
from cart import Cart
from utils.SubscriptionManager import SubscriptionManager
from lifetime.models import *
from account.models import *
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt 
from django.db.models import F
import json


def view_product(request, slug):
    supply = Supply.objects.get(url_slug=slug) 


    template_values = {
        "title": supply.name + " | Lifetime Supply",
        "supply" : supply
    }


    return direct_to_template(request, 'supply_page.html',
                             template_values)

def shop(request):
    subscriptions = request.user.profile.get_subscriptions()
    
    # print request.user.subscription_set.all().values_list('supply__categories', flat=True)
    supplys = [sub.supply for sub in subscriptions]
    categories = sum([list(sup.categories.all()) for sup in supplys], [])

    template_values = {
        "supplys": supplys,
        "categories": categories
    }  

    return direct_to_template(request, 'shop.html',
                             template_values)	







