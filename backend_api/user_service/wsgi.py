import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')  # Змінено з 'backend_api.user_service.settings' на 'settings'
application = get_wsgi_application()