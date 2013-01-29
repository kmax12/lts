from utils.SubscriptionManager import SubscriptionManager
from reg_form import UserRegistrationForm
from lifetime.models import *

def user_created(sender, user, request, **kwargs):
    form = UserRegistrationForm(request.POST)
    code = form.data['code']
    user.first_name = form.data['name']
    user.save()
    if code:
        # try:
        gift = Gift.objects.filter(code=code)         
        if gift.exists():
            s, created = Subscription.objects.get_or_create(user = user, product=gift.product, length_days=gift.length_days)
            gift.subscription = s
            gift.save()
        # except:
        #     pass

print 'loaded'
from registration.signals import user_registered
user_registered.connect(user_created)