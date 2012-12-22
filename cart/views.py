from django.views.generic.simple import direct_to_template
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

@login_required
def checkout(request):
    cart = Cart(request)
    total = cart.total()
    card_id = request.POST.get("card_id", None)
    success = False

    if (request.user and card_id and total > 0 and Card.objects.filter(owner=request.user).exists()):
        sm = SubscriptionManager(request)
        success = sm.charge(cart.total(), card_id)
        if success:
            cart.checkout()
            for item in cart:
                    sm.add(item.get_product(), 365, cart.is_gift()) #todo un hardcode sub length


    template_values = {
        "total" : total
    }


    if success:
        return direct_to_template(request, 'checkout-success.html', template_values)
    else:
        return redirect("cart.views.view_cart")

def add_to_cart(request):
    quantity = 1
    product_id = request.GET.get('id', None)
    if (product_id):
        product = Product.objects.get(id=product_id)
        cart = Cart(request)
        cart.add(product, product.price, quantity)
        
    return redirect('cart.views.view_cart')

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
        "title": "Checkout | Lifetime Supply"
    }

    #switch cart type to gift
    gift = request.GET.get("gift", None)
    if gift:
        Cart(request).set_gift(gift==True)
        return redirect("cart.views.view_cart")
        
    return direct_to_template(request, 'cart.html', template_values)