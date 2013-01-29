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

def home(request):
    if request.user.is_authenticated() and request.GET.get("src", None) != "click":
        return redirect("lifetime.views.shop")

    template_values = {
                    "title": "Lifetime Supply",
                    "home_active" : "active",
                    "supplys": Supply.objects.all(),
                }

    return direct_to_template(request, 'home.html',
                             template_values)

def view_supply(request, slug):
    supply = Supply.objects.get(url_slug=slug) 


    template_values = {
        "title": supply.name + " | Lifetime Supply",
        "supply" : supply
    }


    return direct_to_template(request, 'supply_page.html',
                             template_values)

def view_product(request, slug):
    product = Product.objects.get(id=slug) 

    similar = Product.objects.filter(categories__in=product.categories.all()).exclude(pk=product.pk)

    template_values = {
        "title": product.name + " | Lifetime Supply",
        "product": product,
        "similar": similar
    }

    return direct_to_template(request, 'product_page.html',
                             template_values)

def shop(request):
    subscriptions = request.user.profile.get_subscriptions()
    supplys = [sub.supply for sub in subscriptions]

    request_supply = request.GET.get("supply", None)
    if request_supply:
        try:
            request_supply = request.user.subscription_set.select_related().get(supply__url_slug = request_supply).supply
        except:
            request_supply = None


    #filter out supply 
    if request_supply:
        categories = list(request_supply.categories.all())
    else:
        categories = [list(sup.categories.all()) for sup in supplys] # print request.user.subscription_set.all().values_list('supply__categories', flat=True)
        categories = sum(categories, []) #flatten
    
    request_cat = request.GET.get("cat", None)
    if request_cat:
        request_cat = Category.objects.select_related().get(url_slug = request_cat)
        try:
            request_cat = Category.objects.select_related().get(url_slug = request_cat)
            categories = [request_cat]
            print request_cat
        except:
            request_cat = None

    if request_cat: 
        #filter out supply's that don't fit requested category
        a = set(request_cat.supply_set.all())
        b = set(supplys)
        supplys = list(set(a) & set(b))
        
    #get list of distinct categories
    categories = set(categories)

    template_values = {
        "supplys": supplys,
        "categories": categories,
        "shop_active": "active",
        "request_supply" : request_supply,
        "request_cat" : request_cat
    }  

    return direct_to_template(request, 'shop.html',
                             template_values)	







