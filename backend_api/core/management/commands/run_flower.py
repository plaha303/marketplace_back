from django.core.management.base import BaseCommand
from celery import Celery

class Command(BaseCommand):
    help = 'Run Celery Flower'

    def handle(self, *args, **options):
        from backend_api.celery import celery_app
        celery_app.start(['flower', '--port=5556'])
