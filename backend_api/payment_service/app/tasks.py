from celery import shared_task
from .models import Payment
import logging

logger = logging.getLogger(__name__)

@shared_task(name="payment_service.tasks.process_payment")
def process_payment(payment_id):
    try:
        payment = Payment.objects.get(id=payment_id)
        # Заглушка: імітуємо успішний платіж
        payment.status = 'completed'
        payment.save()
        logger.info(f"Payment {payment_id} processed successfully")
    except Payment.DoesNotExist:
        logger.error(f"Payment {payment_id} not found")
    except Exception as e:
        logger.error(f"Failed to process payment {payment_id}: {str(e)}")