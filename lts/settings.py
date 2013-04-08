# Django settings for lts project.
import os
DEBUG = False
try:
    from local_settings import *
except ImportError:
    pass
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('Max Kanter', 'kmax12@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'kanter+lts',                      # Or path to database file if using sqlite3.
        'USER': 'kanter',                      # Not used with sqlite3.
        'PASSWORD': 'lts12',                  # Not used with sqlite3.
        'HOST': 'sql.mit.edu',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

IGNORABLE_404_ENDS = ('.ico')
IGNORABLE_404_ENDS = ('404.html')

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
STATIC_ROOT = os.path.join(SITE_ROOT, 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'c)-cj-##==1gtihfi$v^jf6f#je$cea!6vc$2t-s2er9-o_p+2'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

AUTHENTICATION_BACKENDS = (
    'lts.email-auth.EmailBackend',
 )

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware', ##fix before going to production
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'lts.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'lts.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'lifetime',
    # 'less',
    'registration',
    'cart',
    'utils',
    'account',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    'south',
    'tastypie',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

TEMPLATE_CONTEXT_PROCESSORS = {
    'django.contrib.messages.context_processors.messages',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.static',
    'utils.context_processors.cart',
    'utils.context_processors.debug',
    'django.core.context_processors.request',
}

ACCOUNT_ACTIVATION_DAYS = 7 # One-week activation window; 

AUTH_PROFILE_MODULE = "account.UserProfile"
LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
LOGIN_REDIRECT_URL = '/account/'
ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda o: "/account/",
}
REGISTRATION_OPEN=True

ORDER_TEXT = "Ship it!"

STRIPE_KEY = "pk_live_mnjoApYz5X91FsZcdyBzjSiw"
STRIPE_SECRET = "sk_live_kqMFbpyk6UhnaMaxOhher2RX"

if DEBUG :
    STRIPE_KEY = "pk_test_K9TEaiWEhLWxOhkmsRC1WgCD"
    STRIPE_SECRET = "sk_test_zRgqAeLfEjLZbD7gnkMIZ3iB"

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'lifetime'
EMAIL_HOST_PASSWORD = 'lifetime12'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


try:
    from local_settings import *
except ImportError:
    pass
