from manage_content_service.settings.base import *

DEBUG = get_environment_var('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = get_environment_var('ALLOWED_HOSTS', '*').split(',')

SERVICE_DOMAIN = get_environment_var(
    'SERVICE_DOMAIN', 'https://cms.sepid.org/')

DB_NAME = get_environment_var('DB_NAME', 'workshop')
DB_USER = get_environment_var('DB_USER', 'user')
DB_PASS = get_environment_var('DB_PASS', 'p4s$pAsS')
DB_HOST = get_environment_var('DB_HOST', 'localhost')
DB_PORT = get_environment_var('DB_PORT', '5432')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASS,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
    }
}

RD_HOST = get_environment_var("RD_HOST", 'redis://0.0.0.0:6379')

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': RD_HOST,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, 'media'),
# )

LOG_LEVEL = get_environment_var('LOG_LEVEL', 'INFO')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s] %(levelname)-8s [%(module)s:%(funcName)s:%(lineno)d]: %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(BASE_DIR, 'logging/debug.log'),
        },
    },
    'loggers': {
        '': {
            'handlers': ['file', 'console'],
            'level': LOG_LEVEL,
            'propagate': True
        },
        'django': {
            'handlers': ['file', 'console'],
            'level': LOG_LEVEL,
            'propagate': True,
        },
        'manage_content_service': {
            'handlers': ['file', 'console'],
            'level': LOG_LEVEL,
            'propagate': True,
        },
    },
}

TESTING = False


ZARINPAL_CONFIG = {
    'ROUTE_START_PAY': 'https://www.zarinpal.com/pg/StartPay/',
    'ROUTE_WEB_GATE': 'https://www.zarinpal.com/pg/services/WebGate/wsdl',
    'TEAM_FEE': int(get_environment_var('TEAM_FEE', '255000')),  # Required
    'PERSON_FEE': int(get_environment_var('PERSON_FEE', '100000')),  # Required
    'MERCHANT': '817461df-e332-4657-85d1-76e7e0a06f0e',  # Required
    'DESCRIPTION': ''  # Required
}

SWAGGER_URL = f'{SERVICE_DOMAIN}api/'

CSRF_TRUSTED_ORIGINS = get_environment_var(
    'CSRF_TRUSTED_ORIGINS', '*').split(',')

DEFAULT_FILE_STORAGE = "minio_storage.storage.MinioMediaStorage"
STATICFILES_STORAGE = "minio_storage.storage.MinioStaticStorage"

MINIO_STORAGE_ENDPOINT = get_environment_var('MINIO_STORAGE_ENDPOINT', None)
MINIO_STORAGE_ACCESS_KEY = get_environment_var(
    'MINIO_STORAGE_ACCESS_KEY', None)
MINIO_STORAGE_SECRET_KEY = get_environment_var(
    'MINIO_STORAGE_SECRET_KEY', None)
MINIO_STORAGE_USE_HTTPS = True
MINIO_STORAGE_MEDIA_BUCKET_NAME = 'media'
MINIO_STORAGE_STATIC_BUCKET_NAME = 'static'
MINIO_STORAGE_AUTO_CREATE_MEDIA_BUCKET = True
MINIO_STORAGE_AUTO_CREATE_STATIC_BUCKET = True
