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
        parser.add_argument(
            '-Q',
            '--queue',
            default=None,
            help='Queue(s) to process (comma-separated, e.g., default,emails)',
        )
        parser.add_argument(
            '--hostname',
            default='worker@%h',
            help='Hostname for the Celery worker (e.g., worker-default@%h)',
        )

    def handle(self, *args, **options):
        from backend_api.celery import celery_app

        queues = options['queue'].split(',') if options['queue'] else None

        worker = celery_app.Worker(
            loglevel=options['loglevel'].upper(),
            hostname=options['hostname'],
            queues=queues,
        )
        worker.start()