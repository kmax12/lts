from django.views.generic.simple import direct_to_template
from utils.SubscriptionManager import SubscriptionManager
from lifetime.models import Order, Product, Subscription
from account.models import AddressForm, Card
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt 
import json

@login_required    
def account(request):
    template_values = {
        'form': AddressForm(),
        'account_active': "active",
        'title': "Account | Lifetime Supply"
    }

    return direct_to_template(request, 'account.html', template_values)

@login_required
def add_card(request):
    token = request.GET.get('token', None)
    success = False

    if (request.user and token):
        sm = SubscriptionManager(request)
        success =  sm.add_card(token)

    return HttpResponse(json.dumps({'success':success}), mimetype="application/json")




@login_required
def order_history(request):
    template_values = {
        'orders': Order.objects.select_related().filter(subscription__owner = request.user),
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
    address.owner = request.user
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
    s = Subscription.objects.get(owner=request.user, product=product)
    
    order = Order(subscription=s)
    order.save()

    template_values = {
        'product': product
    }

    return direct_to_template(request, 'order-success.html', template_values) 