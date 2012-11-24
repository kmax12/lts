from django.views.generic.simple import direct_to_template
# from utils import cart
from cart import Cart
from utils.SubscriptionManager import SubscriptionManager
from lifetime.models import *
from django.http import HttpResponse
from django.shortcuts import redirect
import json


def home(request):
    template_values = {
        "title": "Lifetime Supply",
        "home_active" : "active",
        "products": Product.objects.all()
    }

    return direct_to_template(request, 'home.html',
                             template_values)


def add_to_cart(request):
    quantity = 1
    product_id = request.GET.get('id', None)
    if (product_id):
        product = Product.objects.get(id=product_id)
        cart = Cart(request)
        cart.add(product, product.price, quantity)
        
    return redirect('lifetime.views.view_cart')

def remove_from_cart(request):
    product_id = request.GET.get('id', None)
    response_data = {}
    response_data['success'] = False
    if (product_id):
        product = Product.objects.get(id=product_id)
        cart = Cart(request)
        cart.remove(product)
        response_data['success'] = True

    
    response_data['total'] = cart.total()

    return HttpResponse(json.dumps(response_data), mimetype="application/json")
def view_cart(request):
    template_values = {
        "title": "Checkout | Lifetime Supply",
    }
    return direct_to_template(request, 'cart.html', template_values)

def add_card(request):
    token = request.GET.get('token', None)
    success = False

    if (request.user and token):
        sm = SubscriptionManager(request)
        success =  sm.add_card(token)

    return HttpResponse(json.dumps({'success':success}), mimetype="application/json")

def checkout(request):
    cart = Cart(request)
    total = cart.total()
    success = False
    if (request.user and total > 0 and request.user.profile.stripe_id != ''):
        sm = SubscriptionManager(request)
        success = sm.charge(cart.total())
        if success:
            cart.checkout()
            for item in cart:
                sm.add(item.get_product(), 365) #todo un hardcode sub length


    return HttpResponse(json.dumps({'success':success}), mimetype="application/json")



"""
Content only pages
"""

def how(request):
    template_values = {
        "title": "How it works | Lifetime Supply",
        "how_active" : "active",
    }

    return direct_to_template(request, 'how.html',
                              template_values)

def about(request):
    template_values = {
        "title": "About us | Lifetime Supply",
        "about_active" : "active",
    }

    return direct_to_template(request, 'about.html',
                              template_values)
def faq(request):
    template_values = {
        "title": "FAQ | Lifetime Supply",
        "faq_active" : "active",
    }

    return direct_to_template(request, 'faq.html',
                              template_values)
