# order_service/app/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import requests
import logging

logger = logging.getLogger(__name__)

@shared_task(name="order_service.tasks.send_order_status_update_email")
def send_order_status_update_email(order_id, status):
    try:
        order = Order.objects.get(id=order_id)
        response = requests.get(f"{settings.USER_SERVICE_URL}/users/{order.customer_id}")
        response.raise_for_status()
        user = response.json()
        send_mail(
            f'Order #{order_id} Status Update',
            f'Your order #{order_id} has been updated to {status}.',
            settings.DEFAULT_FROM_EMAIL,
            [user['email']],
            fail_silently=False,
        )
        logger.info(f"Email sent for order {order_id} to {user['email']}")
    except Exception as e:
        logger.error(f"Failed to send email for order {order_id}: {str(e)}")
