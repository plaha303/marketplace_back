# order_service/app/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import requests
import logging

logger = logging.getLogger(__name__)


@shared_task(name="order_service.tasks.send_order_status_update_email", bind=True, max_retries=3, rate_limit='1/m')
def send_order_status_update_email(self, order_id, status):
    try:
        order = Order.objects.get(id=order_id)
        # Отримати email користувача
        response = requests.get(f"{settings.USER_SERVICE_URL}/users/{order.customer_id}", timeout=5)
        response.raise_for_status()
        user = response.json()

        # Отримати статус платежу
        payment_response = requests.get(f"{settings.PAYMENT_SERVICE_URL}/payments/?order_id={order_id}", timeout=5)
        payment_response.raise_for_status()
        payment_status = payment_response.json()[0]['status'] if payment_response.json() else 'pending'

        # Отримати статус доставки
        shipping_response = requests.get(f"{settings.SHIPPING_SERVICE_URL}/shipping/?order_id={order_id}", timeout=5)
        shipping_response.raise_for_status()
        shipping_status = shipping_response.json()[0]['status'] if shipping_response.json() else 'pending'

        # Надіслати email
        message = (
            f"Your order #{order_id} has been updated to {status}.\n"
            f"Payment status: {payment_status}\n"
            f"Shipping status: {shipping_status}"
        )
        send_mail(
            f'Order #{order_id} Status Update',
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user['email']],
            fail_silently=False,
        )
        logger.info(f"Email sent for order {order_id} to {user['email']}")
    except requests.RequestException as e:
        logger.error(f"Failed to fetch data for order {order_id}: {str(e)}")
        self.retry(countdown=60)
    except Exception as e:
        logger.error(f"Failed to send email for order {order_id}: {str(e)}")
        self.retry(countdown=60)