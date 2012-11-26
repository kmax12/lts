from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^account/$', 'lifetime.views.account', name="show account"),
    url(r'^account/history/$', 'lifetime.views.order_history', name="show order history"),
    url(r'^account/address/add/$', 'lifetime.views.add_address', name="add_address"),
    url(r'^account/order/$', 'lifetime.views.place_order', name="place_order"),

    url(r'^cart/add/$', 'lifetime.views.add_to_cart', name="add to cart"),
    url(r'^cart/remove/$', 'lifetime.views.remove_from_cart', name="remove from cart"),
    url(r'^cart/add-card/$', 'lifetime.views.add_card', name="add card to user"),
    url(r'^cart/checkout/$', 'lifetime.views.checkout', name="checkout"),
    url(r'^cart/$', 'lifetime.views.view_cart', name="view_cart"),


    url(r'^how/$', 'lifetime.views.how', name='how'),
    url(r'^about/$', 'lifetime.views.about', name='about'),
    url(r'^faq/$', 'lifetime.views.faq', name='faq'),
    url(r'^contact/$', 'lifetime.views.contact', name='contact'),
    url(r'^$', 'lifetime.views.home', name='home')
    # Examples:
    # url(r'^$', 'lts.views.home', name='home'),
    # url(r'^lts/', include('lts.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
