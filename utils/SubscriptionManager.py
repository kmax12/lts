from account.models import *
from lifetime.models import *
from lts.settings import STRIPE_SECRET, STRIPE_KEY
from utils.registration import email_student_supplies, create_user_with_subscriptions, send_reciept
import stripe
from django.contrib.auth import authenticate, login

stripe.api_key = STRIPE_SECRET

def checkout(request, cart, student, name, customer, email, student_email=None, password=None):
    print cart
    c = charge_customer(cart.total(), customer["id"], email)

    cart.checkout()
    
    send_reciept(
        total = cart.total(),
        supplies = cart.get_supplies(),
        to_email = email,
        name = name,
    )


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

def make_stripe_customer(token, email):
    customer =  stripe.Customer.create(
        card = token,
        description = email
    )

    return customer

def get_stripe_customer(customer_id):
    customer =  stripe.Customer.retrieve(
        customer_id
    )

    return customer

def charge_customer(total, customer_id, email):
    charge = stripe.Charge.create(
                amount= int(total*100), # in cents
                currency= "usd",
                customer= customer_id,
                description= email
            )
    return charge

class SubscriptionManager:
    def __init__(self, request):
        self.user = request.user

    def add(self, supply, length, gift=False):
        created = False
        if self.user:
            if gift:
                 raise Exception('gift checkout not implemented')# sub, created = Gift.objects.get_or_create(owner = self.user, product=product, length_days=length)
            else:
                sub, created = Subscription.objects.get_or_create(owner = self.user, supply=supply, length_days=length)
        print sub                
        return created
    def get_subscriptions(self):
        return Subscription.object.filter(user = self.user)

    def place_order(self, subscription):
        created = False

        if subscription.user == self.user:
            order, created = Order.objects.create(subscription = subscription)

        return created

    def add_card(self, token):
        #todo : store last for and exp dates!
        customer = make_stripe_customer(token, self.user.email)
        print customer
        card = Card(owner=self.user, token=token, last4=customer["active_card"]["last4"], card_type=customer["active_card"]["type"], stripe_id=customer["id"])
        card.save()


        return True


    def charge(self, total, card_id):
        card = Card.objects.filter(owner=self.user, id=card_id) #must filter by user to ensure user own card
        if (card.count() == 0):
            return False
            
        card = card[0]
        if card.stripe_id != '':
            # charge the Customer instead of the card
            charge = stripe.Charge.create(
                amount=int(total*100), # in cents
                currency="usd",
                customer=card.stripe_id,
                description=self.user.email
            )

            profile = self.user.profile
            profile.prefered_card = card_id
            profile.save()

            return True

        return False


