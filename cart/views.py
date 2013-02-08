from django.views.generic.simple import direct_to_template
from cart import Cart
from utils.SubscriptionManager import SubscriptionManager, make_stripe_customer, get_stripe_customer, charge_customer
from lifetime.models import *
from account.models import *
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt 
from django.db.models import F
from utils.registration import email_student_supplies, create_user_with_subscriptions
from django.contrib.auth import authenticate, login
import json

def checkout(request, cart, student, name, customer, email, student_email=None, password=None):
    c = charge_customer(cart.total(), customer["id"], email)



    if student:
        email_student_supplies(
            supplies = cart.get_supplies(),
            from_name = name,
            to_email = student_email
        )
    else:
        create_user_with_subscriptions(name, email, password, cart.get_supplies())

        user = authenticate(username=email, password=password)
        login(request, user)

    

def confirm_checkout(request):
    cart = Cart(request)
    post = request.POST
    error = ''
    if post:
        student = post.get("student", "0")

        name = post.get("name", '')
        if not name: error += "<p>No name</p>"

        email = post.get("lts-email", '')
        if not email: error += "<p>No email</p>"

        student_email = post.get("student_email", '')
        if not student_email and student == "1": error += "<p>No student email</p>"

        password = post.get("password", '')
        if not password and not student: error += "<p>No password</p>"

        token = post.get("token", '')
        if token:
            customer = make_stripe_customer(token, email)
        if not token:
            customer_id = post.get("customer_id", None)
            customer = None
            if customer_id:
                customer = get_stripe_customer(customer_id)
            else:
                error += "<p>Enter credit card</p>"
        
        tos = post.get("tos", None)
        if tos != None : tos = True
        if not tos : error += "<p>Accept Terms of Use</p>"

        if not error:
            if student == "1":
                c = checkout(
                    request = request,
                    cart = cart,
                    student = True,
                    name = name, 
                    customer = customer,
                    email = email,
                    student_email = student_email
                )
            else:
                c = checkout(
                    request = request,
                    cart = cart,
                    student = False, 
                    name = name,
                    customer = customer,
                    email = email,
                    password = password
                )

            if checkout:
                return direct_to_template(request, 'checkout-success.html')


    else:
        student = request.GET.get("student", 0)
        name = ""
        email = ""
        student_email = ""
        password = ""
        token = ""
        tos = False
        customer = None
    


    template_values = {
        "student": student,
        "name" : name,
        "email" : email, 
        "student_email" : student_email,
        "password" : password,
        "token" : token,
        "tos" : tos,
        "customer" : customer
    }

    if error:
        template_values['error'] = error
    return direct_to_template(request, 'confirm-checkout.html', template_values)

def add_to_cart(request):
    quantity = 1
    supply_id = request.GET.get('id', None)
    if (supply_id):
        supply = Supply.objects.get(id=supply_id)
        cart = Cart(request)
        cart.add(supply, supply.price, quantity)
        
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