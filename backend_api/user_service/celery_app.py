# backend_api/user_service/celery_app.py
from celery import Celery

app = Celery('user_service')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()