from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    
    #all the account management stuff
    url(r'^account/$', 'lifetime.views.account', name="show account"),
    url(r'^account/history/$', 'lifetime.views.order_history', name="show order history"),
    url(r'^account/address/$', 'lifetime.views.address', name="address"),
    url(r'^account/address/add/$', 'lifetime.views.add_address', name="add_address"),
    url(r'^account/order/$', 'lifetime.views.place_order', name="place_order"),
    url(r'^account/card/$', login_required(direct_to_template), {'template': 'edit_cards.html', 'extra_context':{'card_active': 'active'}}),
    url(r'^account/cancel/$', login_required(direct_to_template), {'template': 'cancel_subscription.html', 'extra_context':{'cancel_active': 'active'}}),


    #cart stuff
    url(r'^cart/add/$', 'lifetime.views.add_to_cart', name="add to cart"),
    url(r'^cart/remove/$', 'lifetime.views.remove_from_cart', name="remove from cart"),
    url(r'^cart/add-card/$', 'lifetime.views.add_card', name="add card to user"),
    url(r'^cart/checkout/$', 'lifetime.views.checkout', name="checkout"),
    url(r'^cart/$', 'lifetime.views.view_cart', name="view_cart"),



    #static pages
    url(r'^how/$', direct_to_template,{'template': 'how.html', 'extra_context': {"title": "How it works | Lifetime Supply", "how_active" : "active"}}),
    url(r'^about/$', direct_to_template,{'template': 'about.html', 'extra_context': {"title": "About us | Lifetime Supply", "about_active" : "active"}}),
    url(r'^faq/$', direct_to_template,{'template': 'faq.html', 'extra_context': {"title": "FAQ | Lifetime Supply", "faq_active" : "active"}}),
    url(r'^contact/$', direct_to_template,{'template': 'contact.html', 'extra_context': {"title": "Contact | Lifetime Supply", "contact_active" : "active"}}),


    #home
    url(r'^$', 'lifetime.views.home', name='home')
    # Examples:
    # url(r'^$', 'lts.views.home', name='home'),
    # url(r'^lts/', include('lts.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
