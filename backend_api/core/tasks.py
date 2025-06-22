from celery import shared_task
from django.utils.timezone import now
from datetime import timedelta
from .models import User
import logging

logger = logging.getLogger(__name__)

@shared_task
def delete_unverified_users():
    """
    Видаляє неверифікованих користувачів, у яких verification_token_created_at старше 24 годин.
    """
    try:
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