from django.views.generic.simple import direct_to_template
from cart import Cart
from utils.SubscriptionManager import SubscriptionManager, make_stripe_customer, get_stripe_customer, charge_customer, checkout
from lifetime.models import *
from account.models import *
from models import CheckoutStudent, CheckoutSelf, EmailForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt 
from django.db.models import F
from django.contrib.auth import authenticate, login
import json
from django.forms.util import ErrorList

import analytics

def get_email(request):
    post = request.POST
    form = EmailForm()
    if post:
        form = EmailForm(post)
        if form.is_valid():
            request.session['email'] = form.cleaned_data["email"]
            cart = Cart(request)
            cart.cart.email = form.cleaned_data["email"]
            cart.cart.save()
            print request.GET.get('next', '/')
            return HttpResponseRedirect(request.GET.get('next', '/'))

    template_values = {
        'form' : form
    }
    return direct_to_template(request, 'get_email.html', template_values)


def confirm_checkout(request):
    cart = Cart(request)
    post = request.POST
    student = post.get("student", "0")
    if post:
        if student == "1":
            form = CheckoutStudent(post)
        else:
            form = CheckoutSelf(post)

        form.is_valid()
        
        token = post.get("token", '')
        if token:
            customer = make_stripe_customer(token, form.data["email"])
        if not token:
            customer_id = post.get("customer_id", None)
            customer = None
            if customer_id:
                customer = get_stripe_customer(customer_id)
            else:
                form._errors["Credit Card"] = form.error_class(["Please enter credit card"])
        
        if form.is_valid():
            customer.email = form.cleaned_data["email"]
            customer.save()
            if student == "1":
                c = checkout(
                    request = request,
                    cart = cart,
                    student = True,
                    name = form.cleaned_data["name"], 
                    customer = customer,
                    email = form.cleaned_data["email"],
                    student_email = form.cleaned_data["student_email"],
                )
            else:
                c = checkout(
                    request = request,
                    cart = cart,
                    student = False, 
                    customer = customer,
                    name = form.cleaned_data["name"], 
                    email = form.cleaned_data["email"],
                    password = form.cleaned_data["password"],
                )


            return direct_to_template(request, 'checkout-success.html', {"student": student, "total": cart.total(), "email" : form.cleaned_data["email"] })

    else:
        student = request.GET.get("student", 0)
        email = request.session.get('email', '')
        if student == "1":
            form = CheckoutStudent(initial={'email': email})
        else:
            form = CheckoutSelf(initial={'email': email})
        customer = None
    


    template_values = {
        "form" : form,
        "student" : student,
        "customer" : customer
    }

    return direct_to_template(request, 'confirm-checkout.html', template_values)

def add_to_cart(request):    
    quantity = 1
    supply_id = request.GET.get('id', None)
    if (supply_id):

        user_id = "anon"
        if request.user.id:
            user_id = request.user.id


        supply = Supply.objects.get(id=supply_id)
        

        cart = Cart(request)
        cart.add(supply, supply.price, quantity)

        analytics.track(user_id, 'Added to cart', {
          'supply_id' : supply.id,
          "supply_name" : supply.name
        })
        
    if request.session.get('email', '') == '':
        return redirect('cart.views.get_email')

    return redirect('cart.views.view_cart')

def remove_from_cart(request):
    supply_id = request.GET.get('id', None)
    response_data = {}
    response_data['success'] = False
    if (supply_id):
        supply = Supply.objects.get(id=supply_id)
        cart = Cart(request)
        cart.remove(supply)
        response_data['success'] = True

    return redirect('cart.views.view_cart')

def view_cart(request):
    template_values = {
        "title": "Checkout | Lifetime Supply"
    }

    #switch cart type to gift
    gift = request.GET.get("gift", None)
    if gift == '0' or gift == "1":
        gift = True if gift == "1" else False
        Cart(request).set_gift(gift=gift)
        return redirect("cart.views.view_cart")
        
    return direct_to_template(request, 'cart.html', template_values)