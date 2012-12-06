from utils.SubscriptionManager import SubscriptionManager
from reg_form import UserRegistrationForm
from utils.models import *

def user_created(sender, user, request, **kwargs):
    form = UserRegistrationForm(request.POST)
    code = form.data['code']
    print "asdasd"
    print code
    if code:
        # try:
        gift = GiftModel.objects.get(code=code)         
        s, created = Subscription.objects.get_or_create(user = user, product=gift.product, length_days=gift.length_days)
        gift.subscription = s
        gift.save()
        # except:
        #     pass

print 'loaded'
from registration.signals import user_registered
user_registered.connect(user_created)