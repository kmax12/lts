from django.views.generic.simple import direct_to_template
from utils.SubscriptionManager import SubscriptionManager
from lifetime.models import *
from account.models import AddressForm, Card
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt 
import json
import analytics

@login_required    
def account(request):
    orders_raw = request.user.profile.get_orders()
    orders = []
    for i, o in enumerate(orders_raw):
        #has_product_id returns the product instance, match against instance for boolean
        if(o.product.active and request.user.profile.has_product_id(o.product.id) == o.product):
            orders.append( {'obj': o, 'can_order':True} )
        elif(not o.product.active):
            sim_cats = o.product.similar_categories(request.user)
            #TODO: This breaks for products in more than one cat
            shop_url = '/shop/?cat='+sim_cats[0].url_slug
            orders.append( {'obj': o, 'can_order':False, 'shop_url': shop_url} )
        else:
            orders.append( {'obj': o, 'can_order':False} )

    template_values = {
        'form': AddressForm(),
        'account_active': "active",
        'title': "Account | Lifetime Supply",
        'orders': orders
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

        name = request.POST.get('name', '')
        if name != request.user.first_name:
            request.user.first_name = name
            request.user.save()

        
    template_values = {
        'form': AddressForm(instance=request.user.address),
        'name' : request.user.first_name,
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
        return redirect('account.views.account')


    product = request.user.profile.has_product_id(product_id)

    success = False
    if product:
        # subscriptions_used = Subscription.objects.filter(
        #     owner = request.user,
        #     supply__in = Supply.objects.filter(
        #         categories__in = product.categories.all()
        #     )
        # )
        analytics.identify(request.user.id, {
               'email': request.user.email,
               'name': request.user.first_name,
        })

        analytics.track(request.user.id, 'Placed an order', {
          'product_id' : product.id,
          'product_name' : product.name,
        })

        order = Order(user=request.user, product=product)
        order.save()
        success = True

        
    template_values = {
                'product': product,
                'success' : success
            }
    return direct_to_template(request, 'order-success.html', template_values) 