FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY wait-for-db.sh /wait-for-db.sh
RUN chmod +x /wait-for-db.sh

CMD ["/wait-for-db.sh", "marketplace_database", "5432", "sh", "-c", "python manage.py makemigrations app && python manage.py migrate --noinput && gunicorn --bind 0.0.0.0:8000 wsgi:application"]