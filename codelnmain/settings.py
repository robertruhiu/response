"""
Django settings for codelnmain project on Heroku. For more info, see:
https://github.com/heroku/heroku-django-template

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
from builtins import bool
import datetime
import dj_database_url
import django_heroku
from decouple import config

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

SECRET_KEY = config('SECRET_KEY', default='SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ENVIRONMENT = config('ENVIRONMENT', default='local')

# SECURITY WARNING: keep the secret key used in production secret!
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'accounts',
    'projects',
    'frontend',
    'taggit',
    'classroom',
    'blog',
    'django.contrib.admindocs',
    'cloudinary_storage',
    'cloudinary',

    'transactions',
    'payments',
    'marketplace',
    'crispy_forms',

    # third party libs
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    # 'django_filters',
    'invitations',
    'allauth.socialaccount.providers.linkedin',
    'storages',
    'bootstrap4',
    'django_forms_bootstrap',
    'django_countries',
    'phonenumber_field',
    'celery',
    'ckeditor',
    'ckeditor_uploader',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'rest_auth',
    'rest_auth.registration',

]
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',

    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}

JWT_AUTH = {
    'JWT_VERIFY': True,
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_LEEWAY': 0,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=86400),
    'JWT_ALLOW_REFRESH': True,
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),
}

CORS_ORIGIN_WHITELIST = (
    'http://localhost:8000',
    'http://localhost:8080',
    'http://localhost:8081',
    'http://localhost:8082',
    'https://mulan.herokuapp.com',
    'https://leanapp.herokuapp.com',
    'http://mulan.herokuapp.com',
    'http://leanapp.herokuapp.com',

)

REST_USE_JWT = True
# Application definition
SITE_ID = 1

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'codelnmain.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media'
            ],
            'debug': DEBUG,
        },
    },
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

WSGI_APPLICATION = 'codelnmain.wsgi.application'

# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'mrembo',
#         'USER': 'postgres',
#         'PASSWORD': 'Pokerface1994',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'delfm8a38hujqh',
#         'USER': 'zwoyihgclnpxxl',
#         'PASSWORD': 'b8c1c02d756826889dd0c32024144b07f7e09216b6b225ab73a19f2ae92b20a3',
#         'HOST': 'ec2-54-228-207-163.eu-west-1.compute.amazonaws.com',
#         'PORT': '5432',
#     }
# }
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'dbeqvronr59rp3',
#         'USER': 'unyokuvzspuixp',
#         'PASSWORD': 'e2c5c2d852cca022ee1e09b7c2bba04a0b08acbeeb2f1c6ef8c6db1efd1bb7c8',
#         'HOST': 'ec2-54-217-234-157.eu-west-1.compute.amazonaws.com',
#         'PORT': '5432',
#     }
# }


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Change 'default' database configuration with $DATABASE_URL.
DATABASES['default'].update(dj_database_url.config(conn_max_age=500, ssl_require=True))

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=lambda v: [
    s.strip() for s in v.split(',')], default='*')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, 'static'),
]

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

# email settings
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='DEFAULT_FROM_EMAIL')
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='EMAIL_HOST_PASSWORD')

# allauth settings
ACCOUNT_AUTHENTICATION_METHOD = ('email')
ACCOUNT_SIGNUP_PASSWORD_VERIFICATION = False
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_CONFIRMATION_HMAC = True
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = None
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3
ACCOUNT_EMAIL_VERIFICATION = "optional"
ACCOUNT_EMAIL_REQUIRED = True
EMAIL_CONFIRMATION_SIGNUP = False
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_LOGOUT_REDIRECT_URL = '/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_URL = '/'
ACCOUNT_SESSION_REMEMBER = None
ACCOUNT_SIGNUP_FORM_CLASS = 'accounts.forms.SignUpForm'
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True
ACCOUNT_EMAIL_CONFIRMATION_COOLDOWN = 600

SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_EMAIL_VERIFICATION = ACCOUNT_EMAIL_VERIFICATION
SOCIALACCOUNT_EMAIL_REQUIRED = ACCOUNT_EMAIL_REQUIRED
SOCIALACCOUNT_QUERY_EMAIL = ACCOUNT_EMAIL_REQUIRED
SOCIALACCOUNT_PROVIDERS = {
    'linkedin': {
        'SCOPE': [
            'r_basicprofile',
            'r_emailaddress'
        ],
        'PROFILE_FIELDS': [
            'id',
            'first-name',
            'last-name',
            'email-address',
            'picture-url',
            'public-profile-url',
        ]
    }
}

ACCOUNT_ADAPTER = 'invitations.models.InvitationsAdapter'
INVITATIONS_INVITATION_EXPIRY = 7
INVITATIONS_CONFIRM_INVITE_ON_GET = True
INVITATIONS_ALLOW_JSON_INVITES = True
INVITATIONS_ADAPTER = ACCOUNT_ADAPTER
INVITATIONS_EMAIL_SUBJECT_PREFIX = 'Codeln'

AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID', default='AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY', default='AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME', default='AWS_STORAGE_BUCKET_NAME')
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_PUBLIC_MEDIA_LOCATION = 'media/public'
DEFAULT_FILE_STORAGE = 'codelnmain.storage_backends.PublicMediaStorage'

AWS_PRIVATE_MEDIA_LOCATION = 'media/private'
PRIVATE_FILE_STORAGE = 'codelnmain.storage_backends.PrivateMediaStorage'
AWS_DEFAULT_ACL = "public-read"
MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN,
                                AWS_PUBLIC_MEDIA_LOCATION)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

TAGGIT_CASE_INSENSITIVE = True
if ENVIRONMENT != 'local':
    pass

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.RawMediaCloudinaryStorage'

CLOUDINARY = {
    'cloud_name': 'dwtvwjhn3',
    'api_key': '748889632162181',
    'api_secret': 'ecbWIeK33ka7-1wyy9TiB6pVwAw',
}
CLOUDINARY_STORAGE = {

    'CLOUD_NAME': 'dwtvwjhn3',
    'API_KEY': '748889632162181',
    'API_SECRET': 'ecbWIeK33ka7-1wyy9TiB6pVwAw',

}
CKEDITOR_JQUERY_URL = 'https://ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min.js'

CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_IMAGE_BACKEND = "pillow"

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': None,

    },
}
