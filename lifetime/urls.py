from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template
from lifetime.models import Supply
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    #product stuff
    url(r'^supply/(.+)$', 'lifetime.views.view_supply', name="view_cart"),    
    url(r'^shop/$', 'lifetime.views.shop', name="shop"),    
    url(r'^buy-supply/$', 'lifetime.views.buy_supply', name="shop"),    
    url(r'^product/([0-9]+)$', 'lifetime.views.view_product', name="view_cart"),    



    #static pages
    url(r'^how/$', direct_to_template,{'template': 'how.html', 'extra_context': {"title": "How it works | Lifetime Supply", "how_active" : "active"}}),
    url(r'^about/$', direct_to_template,{'template': 'about.html', 'extra_context': {"title": "About us | Lifetime Supply", "about_active" : "active"}}),
    url(r'^faq/$', direct_to_template,{'template': 'faq.html', 'extra_context': {"title": "FAQ | Lifetime Supply", "faq_active" : "active"}}),
    url(r'^contact/$', direct_to_template,{'template': 'contact.html', 'extra_context': {"title": "Contact | Lifetime Supply", "contact_active" : "active"}}),
    url(r'^terms/$', direct_to_template,{'template': 'terms.html', 'extra_context': {"title": "Terms of Use | Lifetime Supply"}}),
    url(r'^privacy/$', direct_to_template,{'template': 'privacy.html', 'extra_context': {"title": "Privacy Policy| Lifetime Supply"}}),
    
    #landing pages
    url(r'^parents/$', direct_to_template,{'template': 'parents.html', 'extra_context': {"title": "For Parents | Lifetime Supply", "elsupplys": Supply.objects.all().order_by('?')[:3]}}),

    # url(r'^$', direct_to_template,{'template': 'signup.html'}),
    url(r'^$', 'lifetime.views.home', name="home"),    
    # Examples:
    # url(r'^$', 'lts.views.home', name='home'),
    # url(r'^lts/', include('lts.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
