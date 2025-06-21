from django.core.management.base import BaseCommand
from celery import Celery

class Command(BaseCommand):
    help = 'Run Celery Beat scheduler'

    def add_arguments(self, parser):
        parser.add_argument(
            '--loglevel',
            default='info',
            help='Log level for Celery Beat (e.g., debug, info, warning, error)',
        )

    def handle(self, *args, **options):
        from backend_api.celery import celery_app
        celery_app.start(['beat', '--loglevel', options['loglevel'].upper()])