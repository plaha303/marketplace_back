from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
app = Celery('payment_service')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()