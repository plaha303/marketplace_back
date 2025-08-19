from pathlib import Path
import environ
import os
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
BASE_DIR = Path(__file__).resolve().parent

env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, ['localhost', '127.0.0.1', 'product_service']),
    FRONTEND_URL=(str, 'http://localhost:3000')
)
environ.Env.read_env(os.path.join(BASE_DIR.parent.parent, '.env'))

SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')
ALLOWED_HOSTS = env('ALLOWED_HOSTS')
logger.info(f"ALLOWED_HOSTS set to: {ALLOWED_HOSTS}")

USER_SERVICE_URL = env('USER_SERVICE_URL', default='http://user_service:8000')
ORDER_SERVICE_URL = env('ORDER_SERVICE_URL', default='http://order_service:8000')
PRODUCT_SERVICE_URL = env('PRODUCT_SERVICE_URL', default='http://product_service:8000')

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': env('CLOUD_NAME'),
    'API_KEY': env('API_KEY'),
    'API_SECRET': env('API_SECRET'),
}
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework_simplejwt.token_blacklist',
    'django.contrib.postgres',
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_spectacular',
    'django_filters',
    'django_celery_beat',
    'cloudinary',
    'app',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'app/templates')],
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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_DATABASE'),
        'USER': env('DB_USERNAME'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': 'marketplace_database',
        'PORT': '5432',
        'OPTIONS': {'options': '-c search_path=product_service'},
    }
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ('rest_framework_simplejwt.authentication.JWTAuthentication',),
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated',),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 50,
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=120),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=14),
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_COOKIE': 'refresh_token',
    'AUTH_COOKIE_HTTP_ONLY': True,
    'AUTH_COOKIE_SECURE': True,
    'AUTH_COOKIE_SAMESITE': 'None',
}

CELERY_BROKER_URL = env('REDIS_URL', default='redis://marketplace_redis:6379/0')
CELERY_RESULT_BACKEND = env('REDIS_URL', default='redis://marketplace_redis:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {'sensitive_data': {'()': 'app.log_filters.SensitiveDataFilter'}},
    'handlers': {
        'console': {'class': 'logging.StreamHandler', 'filters': ['sensitive_data']},
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'product_service.log',
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'backupCount': 5,
            'filters': ['sensitive_data']
        }
    },
    'loggers': {
        'django': {'handlers': ['console', 'file'], 'level': 'INFO', 'propagate': False},
        'app': {'handlers': ['console', 'file'], 'level': 'DEBUG', 'propagate': False},
        '': {'handlers': ['console', 'file'], 'level': 'DEBUG', 'propagate': False},
    },
}

FRONTEND_URL = env('FRONTEND_URL')
CORS_ALLOWED_ORIGINS = ['http://localhost:3000', 'http://localhost:5173']
CORS_ALLOW_CREDENTIALS = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'app/static')]