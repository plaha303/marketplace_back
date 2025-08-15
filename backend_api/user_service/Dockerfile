FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Встановлюємо curl і postgresql-client (для pg_isready)
RUN apt-get update && apt-get install -y curl postgresql-client && rm -rf /var/lib/apt/lists/*

COPY . .

# Копіюємо скрипт wait-for-db.sh в контейнер
COPY wait-for-db.sh /wait-for-db.sh
RUN chmod +x /wait-for-db.sh

# Команда запуску: чекаємо БД, виконуємо міграції, збираємо статичні файли та запускаємо Gunicorn
CMD ["/wait-for-db.sh", "marketplace_database", "5432", "sh", "-c", "python manage.py makemigrations app && python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn --bind 0.0.0.0:8000 wsgi:application"]