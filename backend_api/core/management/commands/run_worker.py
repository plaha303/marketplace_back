from django.core.management.base import BaseCommand
from celery import Celery

class Command(BaseCommand):
    help = 'Run Celery worker'

    def add_arguments(self, parser):
        parser.add_argument(
            '--loglevel',
            default='info',
            help='Log level for Celery worker (e.g., debug, info, warning, error)',
        )

    def handle(self, *args, **options):
        from backend_api.celery import celery_app
        worker = celery_app.Worker(
            loglevel=options['loglevel'].upper(),
            hostname='worker@%h',
        )
        worker.start()