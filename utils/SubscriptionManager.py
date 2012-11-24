from utils.models import *
from lts.settings import STRIPE_KEY
import stripe

stripe.api_key = STRIPE_KEY

class SubscriptionManager:
    def __init__(self, request):
        self.user = request.user

    def add(self, product, length):
        created = False
        if (self.user):
            sub, created = Subscription.objects.get_or_create(user = self.user, product=product, length_days=length)
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
        customer = stripe.Customer.create(
            card=token,
            description= self.user.email
        )

        

        user_profile = self.user.profile
        user_profile.stripe_id = customer['id']

        user_profile.save()


        return True

    def charge(self, total):
        if self.user.profile.stripe_id != '':
            # charge the Customer instead of the card
            charge = stripe.Charge.create(
                amount=int(total*100), # in cents
                currency="usd",
                customer=self.user.profile.stripe_id,
                description=self.user.email
            )


            return True

        return False


