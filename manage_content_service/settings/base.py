import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_environment_var(var_name, default, prefixed=True):
    if prefixed:
        var_name = 'MANAGE_CONTENT_SERVICE_%s' % var_name
    return os.getenv(var_name, default)


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/


# Application definition

DEFAULT_APPS = [
    'corsheaders',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

CUSTOM_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    'import_export',
    'drf_yasg',
    'celery',
    'polymorphic',
    'django_extensions',
    'django_filters',
    'minio_storage',
    'shortener',
    'manage_content_service.apps.MyAdminConfig',
    'apps.accounts.apps.AccountConfig',
    'apps.fsm.apps.FsmConfig',
    'apps.scoring.apps.ScoringConfig',
    'apps.roadmap.apps.RoadmapConfig',
    'apps.contact.apps.ContactConfig',
    'apps.report.apps.ReportConfig',
    'apps.sales.apps.SalesConfig',
    # 'django_cleanup.apps.CleanupConfig', todo: حواسم باشه که فایل‌ها روی درایو می‌مونن
    'apps.file_storage.apps.FileStorageConfig',
    'apps.attributes.apps.AttributesConfig',
    'apps.widgets.apps.WidgetsConfig',
]

INSTALLED_APPS = DEFAULT_APPS + CUSTOM_APPS

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'manage_content_service.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/api/static/'

MEDIA_URL = '/api/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'sepid.platform@gmail.com'
EMAIL_HOST_PASSWORD = 'tmyz glmk cjsj urnw'

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

CONSTANTS = {
    "PAGINATION_NUMBER": 50,
}

# Custom user model
AUTH_USER_MODEL = "accounts.User"

ASGI_APPLICATION = 'manage_content_service.routing.application'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': '18'
}


AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

GUARDIAN_RAISE_403 = True
ANONYMOUS_USER_NAME = None

SWAGGER_SETTINGS = {
    'LOGIN_URL': '/api/auth/accounts/login/',
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    },
    'DEFAULT_AUTO_SCHEMA_CLASS': 'manage_content_service.settings.custom_setting_classes.CustomAutoSchema',
    'TAGS_SORTER': 'alpha',
    'DOC_EXPANSION': 'none',
}

KAVENEGAR_TOKEN = get_environment_var('KAVENEGAR_TOKEN', None)

VOUCHER_CODE_LENGTH = 5

DISCOUNT_CODE_LENGTH = 10

PURCHASE_UNIQ_CODE_LENGTH = 10


########## Celery ##########

CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
ROOT_URLCONF = 'manage_content_service.urls'
CELERY_BROKER_URL = get_environment_var('BROKER_URL', 'amqp://')


########## Zarrinpal Payment ##########

def GET_PAYMENT_CALLBACK_URL(domain, status):
    PAYMENT = {
        'success': f'http://{domain}/message/payment/success',
        'failure': f'http://{domain}/message/payment/failure',
    }
    return PAYMENT[status]


########## METABASE ##########

METABASE_URL = get_environment_var('METABASE_URL', None)
METABASE_USERNAME = get_environment_var('METABASE_USERNAME', None)
METABASE_PASSWORD = get_environment_var('METABASE_PASSWORD', None)


########## INSTANT MESSAGING ##########

INSTANT_MESSAGE_URL = get_environment_var(
    'INSTANT_MESSAGE_URL', 'https://ims.sepid.org/')


########## BAND AS A SERVICE ##########

BANK_URL = get_environment_var('BANK_URL', '"https://bank.sepid.org"')


ASSESS_ANSWER_SERVICE_URL = get_environment_var(
    'ASSESS_ANSWER_SERVICE_URL', 'https://aas.sepid.org/')


########## CORS ##########

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_ALL_ORIGINS = True  # Or specify allowed origins
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Website',  # Add your custom header here
]
