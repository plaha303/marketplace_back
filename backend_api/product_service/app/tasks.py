from celery import shared_task
import cloudinary.uploader
from django.conf import settings
from app.models import Product, ProductImage, Review
from django.core.mail import send_mail
import logging
import requests

logger = logging.getLogger(__name__)

# Список "поганих" слів для заглушки модерації
BAD_WORDS = {'bad', 'offensive', 'inappropriate', 'hate'}

@shared_task(queue='images')
def process_image(product_id, image_data, user_id=None):
    try:
        result = cloudinary.uploader.upload(
            image_data,
            folder=f'products/{product_id}',
            public_id=f'product_{product_id}',
            overwrite=True,
            resource_type='image'
        )
        ProductImage.objects.create(
            product_id=product_id,
            image_url=result['secure_url'],
            user_id=user_id or 0
        )
        logger.info(f"Зображення для продукту {product_id} успішно завантажено: {result['secure_url']}")
    except Exception as e:
        logger.error(f"Помилка обробки зображення для продукту {product_id}: {str(e)}")

@shared_task(queue='auto_moderation')
def auto_moderate_product(product_id):
    try:
        product = Product.objects.get(id=product_id)
        text_to_moderate = f"{product.name} {product.description or ''}".lower()
        is_toxic = any(bad_word in text_to_moderate for bad_word in BAD_WORDS)
        product.is_approved = not is_toxic
        product.save()
        logger.info(f"Модерація продукту {product_id}: is_approved={product.is_approved}")
    except Exception as e:
        logger.error(f"Помилка модерації продукту {product_id}: {str(e)}")

@shared_task(queue='moderation')
def send_moderation_notification(content_type, content_id, is_approved, recipient_email):
    try:
        subject = f"{content_type.capitalize()} {'схвалено' if is_approved else 'відхилено'}"
        message = f"Ваш {content_type} (ID: {content_id}) був {'схвалений' if is_approved else 'відхилений'} адміністратором."
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [recipient_email],
            fail_silently=False,
        )
        logger.info(f"Повідомлення про модерацію відправлено: {content_type} {content_id} для {recipient_email}")
    except Exception as e:
        logger.error(f"Помилка при відправці повідомлення для {content_type} {content_id}: {str(e)}")
        raise

@shared_task(queue='moderation', bind=True, max_retries=3, default_retry_delay=60)
def moderate_content(self, content_type, content_id, content_text):
    try:
        is_toxic = any(bad_word in content_text.lower() for bad_word in BAD_WORDS)
        with transaction.atomic():
            if content_type == 'product':
                obj = Product.objects.get(id=content_id)
            elif content_type == 'review':
                obj = Review.objects.get(id=content_id)
            else:
                raise ValueError(f"Невалідний content_type: {content_type}")
            obj.is_approved = not is_toxic
            obj.save()

        if is_toxic:
            recipient_email = None
            if content_type == 'product':
                response = requests.get(f"{settings.USER_SERVICE_URL}/users/{obj.vendor_id}", timeout=5)
                response.raise_for_status()
                recipient_email = response.json().get('email')
            elif content_type == 'review':
                response = requests.get(f"{settings.USER_SERVICE_URL}/users/{obj.user_id}", timeout=5)
                response.raise_for_status()
                recipient_email = response.json().get('email')

            if recipient_email:
                send_moderation_notification.delay(content_type, content_id, False, recipient_email)
        logger.info(f"Модерація {content_type} {content_id}: is_toxic={is_toxic}")
    except Exception as e:
        logger.error(f"Помилка модерації {content_type} {content_id}: {str(e)}")
        raise self.retry(exc=e)