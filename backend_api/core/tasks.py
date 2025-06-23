from celery import shared_task
from django.utils.timezone import now
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from django.core.cache import cache
from .models import User, Order, EmailLog
from django.db import transaction
from django.template.loader import render_to_string
import logging
import re

logger = logging.getLogger(__name__)

@shared_task(name="core.tasks.delete_unverified_users")
def delete_unverified_users():
    """
    Видаляє неверифікованих користувачів, у яких verification_token_created_at старше 24 годин.
    """
    try:
        with transaction.atomic():
            expiration_time = now() - timedelta(hours=24)
            unverified_users = User.objects.filter(
                is_verified=False,
                verification_token_created_at__lt=expiration_time
            )
            count = unverified_users.count()
            if count > 0:
                unverified_users.delete()
                logger.info(f"Deleted {count} unverified users.")
            else:
                logger.info("No unverified users found for deletion.")
    except Exception as e:
        logger.error(f"Error deleting unverified users: {str(e)}")

def is_throttled(order_id):
    """
    Перевіряє, чи не надто часто надсилаються email для замовлення.
    """
    key = f"email_sent_for_order_{order_id}"
    if cache.get(key):
        logger.warning(f"Email throttled for order {order_id}")
        return True
    cache.set(key, True, timeout=60)  # Блокування на 1 хвилину
    return False

def is_valid_email(email):
    """
    Базова перевірка формату email.
    """
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(email_regex, email))

@shared_task(
    bind=True,
    name="core.tasks.send_order_status_update_email",
    max_retries=5,
    default_retry_delay=60,
    queue="emails"
)
def send_order_status_update_email(self, order_id=None, new_status=None):
    """
    Надсилає email користувачу про зміну статусу замовлення.
    """
    if order_id is None or new_status is None:
        logger.warning("Missing order_id or new_status for send_order_status_update_email task")
        return

    if is_throttled(order_id):
        return

    try:
        with transaction.atomic():
            order = Order.objects.select_for_update().get(id=order_id)
            user = order.customer

            # Перевірка справжності статусу
            if order.status != new_status:
                logger.warning(f"Requested status '{new_status}' does not match actual status '{order.status}' for order {order_id}")
                return

            if not user or not user.email or not is_valid_email(user.email):
                logger.warning(f"No valid user or email for order {order_id}")
                return

            subject = f"Оновлення статусу замовлення #{order_id}"
            message = render_to_string('emails/order_status_update.html', {
                'user': user,
                'order_id': order_id,
                'new_status': new_status,
                'frontend_url': settings.FRONTEND_URL,
            })
            send_mail(
                subject=subject,
                message='',  # Текстова версія порожня, оскільки використовуємо HTML
                html_message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )

            # Збереження логів email
            EmailLog.objects.create(
                order=order,
                recipient=user.email,
                subject=subject,
                status='sent',
                sent_at=now()
            )
            logger.info(f"Order status update email sent to {user.email} for order {order_id}")

    except Order.DoesNotExist:
        logger.error(f"Order {order_id} not found for sending status update email")
    except Exception as e:
        logger.error(f"Error sending order status update email for order {order_id}: {str(e)}")
        # Збереження логів у разі помилки
        try:
            EmailLog.objects.create(
                order_id=order_id,
                recipient=user.email if user else 'unknown',
                subject=subject if 'subject' in locals() else f"Оновлення статусу замовлення #{order_id}",
                status='failed',
                error=str(e),
                sent_at=now()
            )
        except:
            logger.error(f"Failed to log email error for order {order_id}")
        raise self.retry(exc=e)