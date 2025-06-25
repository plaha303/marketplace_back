from celery import shared_task
from django.utils.timezone import now
from datetime import timedelta
import requests
from django.core.mail import send_mail
from django.conf import settings
from django.core.cache import cache
from .models import User, Order, EmailLog, Category, ProductImage
from django.db import transaction
from django.template.loader import render_to_string
import logging
import re
from django.core.files.uploadedfile import SimpleUploadedFile

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


@shared_task(
    bind=True,
    name="core.tasks.upload_image_to_imgbb",
    max_retries=3,
    default_retry_delay=60,
    queue="images"
)
def upload_image_to_imgbb(self, model_type, instance_id, user_id, image_data, image_name):
    """
    Асинхронно завантажуємо зображення до ImgBB і зберігає URL у моделі.

    Args:
        model_type (str): 'category' або 'product'
        instance_id (int): ID категорії або продукту
        user_id (int): ID користувача, який виконує дію
        image_data (bytes): Бінарні дані зображення
        image_name (str): Ім'я файлу зображення
    """
    try:
        url = "https://api.imgbb.com/1/upload"
        params = {
            "key": settings.IMGBB_API_KEY,
            "expiration": settings.IMGBB_EXPIRATION,
            "name": image_name,
        }
        files = {"image": (image_name, image_data)}

        response = requests.post(url, params=params, files=files)
        response.raise_for_status()  # Викликає виняток для статусів 4xx/5xx
        response_data = response.json()

        if not response_data.get("success"):
            logger.error(f"ImgBB upload failed for {model_type} {instance_id}: {response_data}")
            raise Exception(f"ImgBB API error: {response_data.get('error', 'Unknown error')}")

        image_url = response_data["data"]["url"]
        logger.info(f"Image uploaded to ImgBB: {image_url}")

        with transaction.atomic():
            if model_type == "category":
                category = Category.objects.get(id=instance_id)
                category.category_image = image_url
                category.save()
                logger.info(f"Updated category {instance_id} with image URL: {image_url}")
            elif model_type == "product":
                product_image = ProductImage.objects.create(
                    product_id=instance_id,
                    image_url=image_url
                )
                logger.info(f"Created ProductImage for product {instance_id} with URL: {image_url}")
            else:
                raise ValueError(f"Invalid model_type: {model_type}")

        return {"success": True, "image_url": image_url}

    except requests.exceptions.RequestException as e:
        logger.error(f"ImgBB upload failed for {model_type} {instance_id} by user {user_id}: {str(e)}")
        self.retry(exc=e)
    except Exception as e:
        logger.error(f"Error in upload_image_to_imgbb for {model_type} {instance_id} by user {user_id}: {str(e)}")
        raise
