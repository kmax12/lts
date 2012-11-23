from django.views.generic.simple import direct_to_template
# from utils import cart
from cart import Cart
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
    product_id = request.GET.get('id', '0')
    if (product_id != '0'):
        product = Product.objects.get(id=product_id)
        cart = Cart(request)
        cart.add(product, product.price, quantity)
        
    return redirect('lifetime.views.view_cart')

def remove_from_cart(request):
    product_id = request.GET.get('id', '0')
    response_data = {}
    response_data['success'] = False
    if (product_id != '0'):
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

def partial_cart(request):
    return direct_to_template(request, 'cart_content.html')

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
