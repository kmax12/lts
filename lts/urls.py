from django.conf.urls import patterns, include, url
from reg_form import UserRegistrationForm
from registration.views import register
import regbackend

from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
	url(r'^register/$', register, {'backend': 'registration.backends.simple.SimpleBackend','form_class': UserRegistrationForm}, name='registration_register'),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
	(r'', include('registration.backends.simple.urls')),
	url(r'', include('lifetime.urls')),
    # Examples:
    # url(r'^$', 'lts.views.home', name='home'),
    # url(r'^lts/', include('lts.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
