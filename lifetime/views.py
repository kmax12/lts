from django.views.generic.simple import direct_to_template
# from utils import cart
from cart import Cart
from utils.SubscriptionManager import SubscriptionManager
from utils.models import *
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
        "title": "Checkout | Lifetime Supply"
    }

    #switch cart type to gift
    gift = request.GET.get("gift", None)
    if gift:
        Cart(request).set_gift(gift=="1")
        return redirect("lifetime.views.view_cart")
        
    return direct_to_template(request, 'cart.html', template_values)

@login_required
def add_card(request):
    token = request.GET.get('token', None)
    success = False

    if (request.user and token):
        sm = SubscriptionManager(request)
        success =  sm.add_card(token)

    return HttpResponse(json.dumps({'success':success}), mimetype="application/json")

@login_required
def checkout(request):
    cart = Cart(request)
    total = cart.total()
    card_id = request.POST.get("card_id", None)
    success = False

    if (request.user and card_id and total > 0 and Card.objects.filter(user=request.user).count() != 0):
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
        return redirect("lifetime.views.view_cart")

@login_required    
def account(request):
    template_values = {
        'form': AddressForm(),
        'orders_active': "active"
    }

    return direct_to_template(request, 'account.html', template_values)

@login_required
def order_history(request):
    template_values = {
        'orders': Order.objects.select_related().filter(subscription__user = request.user),
    }

    return direct_to_template(request, 'order_history.html', template_values)    

@login_required
@csrf_exempt
def address(request):
    saved = False

    if request.POST:
        saved = True

        form = AddressForm(request.POST, instance=request.user.address)
        a = form.save(commit=False)
        a.edited = True

        a.save()

        print a.edited
        
    template_values = {
        'form': AddressForm(instance=request.user.address),
        'address_active': "active",
        'saved': saved
    }

    return direct_to_template(request, 'edit_address.html', template_values)

@login_required
@csrf_exempt
def add_address(request):
    address = AddressForm(request.POST)
    address = address.save(commit=False)
    address.user = request.user
    address.save()
    success = True

    return HttpResponse(json.dumps({'success':success}), mimetype="application/json")

@login_required
@csrf_exempt
def place_order(request):
    product_id = request.POST.get("id", None)
    if not product_id:
        return redirect('lifetime.views.account')


    product = Product.objects.get(id=product_id)
    s = Subscription.objects.get(user=request.user, product=product)
    
    order = Order(subscription=s)
    order.save()

    template_values = {
        'product': product
    }

    return direct_to_template(request, 'order-success.html', template_values) 




