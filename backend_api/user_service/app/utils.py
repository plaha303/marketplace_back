import logging
from django.db import connection

logger = logging.getLogger(__name__)

def check_database_connection():
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        logger.info("Database connection successful")
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {str(e)}")
        return False