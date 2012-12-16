from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    #all the account management stuff
    url(r'^history/$', 'account.views.order_history', name="show order history"),
    url(r'^address/$', 'account.views.address', name="address"),
    url(r'^address/add/$', 'account.views.add_address', name="add_address"),
    url(r'^order/$', 'account.views.place_order', name="place_order"),
    url(r'^card/$', login_required(direct_to_template), {'template': 'edit_cards.html', 'extra_context':{'card_active': 'active'}}),
    url(r'^cancel/$', login_required(direct_to_template), {'template': 'cancel_subscription.html', 'extra_context':{'cancel_active': 'active'}}),
    url(r'^add-card/$', 'account.views.add_card', name="add card to user"),
    url(r'^$', 'account.views.account', name="show account"),
)
