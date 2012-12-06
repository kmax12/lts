from utils.models import *
from lts.settings import STRIPE_KEY
import stripe

stripe.api_key = STRIPE_KEY

class SubscriptionManager:
    def __init__(self, request):
        self.user = request.user

    def add(self, product, length, gift=False):
        created = False
        if (self.user):
            print gift
            if gift:
                sub, created = GiftModel.objects.get_or_create(user = self.user, product=product, length_days=length)
            else:
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
        print customer
        card = Card(user=self.user, token=token, last4=customer["active_card"]["last4"], card_type=customer["active_card"]["type"], stripe_id=customer["id"])
        card.save()


        return True

    def charge(self, total, card_id):
        card = Card.objects.filter(user=self.user, id=card_id) #must filter by user to ensure user own card
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


