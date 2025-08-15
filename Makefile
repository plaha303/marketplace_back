#!/usr/bin/make

DOCKER_COMPOSE_BIN := $(shell command -v docker-compose 2>/dev/null || echo "docker compose")

# Визначаємо, чи потрібно створити віртуальне оточення
VENV_DIR := .venv
VENV_BIN := $(VENV_DIR)/bin
PYTHON_BIN := $(VENV_BIN)/python
PIP_BIN := $(VENV_BIN)/pip
VENV_ACTIVATE := $(VENV_BIN)/activate
VENV_ACTIVATE_WINDOWS := $(VENV_DIR)/Scripts/activate

# Визначаємо правильний шлях для активації в залежності від ОС
ifeq ($(OS),Windows_NT)
    ACTIVATE := $(VENV_ACTIVATE_WINDOWS)
else
    ACTIVATE := $(VENV_ACTIVATE)
endif

# Перевіряємо, чи активоване віртуальне оточення
check_venv:
	@echo "🔍 Перевіряю, чи активоване віртуальне оточення..."
	@if [ ! -d "$(VENV_DIR)" ]; then \
		echo "❌ Віртуальне оточення не знайдено. Створюю..."; \
		python3 -m venv $(VENV_DIR); \
		. $(ACTIVATE); \
		echo "🛠 Створено та активовано віртуальне оточення..."; \
	elif [ -z "$$VIRTUAL_ENV" ]; then \
		echo "❌ Віртуальне оточення не активоване. Активую..."; \
		. $(ACTIVATE); \
	else \
		echo "✅ Віртуальне оточення вже активоване."; \
	fi

# Встановлення всіх залежностей
install_all: check_venv
	@echo "📦 Встановлення всіх залежностей..."
	$(PIP_BIN) install --no-cache-dir -r backend_api/user-service/requirements.txt

# Повний автоматичний запуск усіх контейнерів
up: install_all
	@echo "🚀 Запуск усіх контейнерів..."
	$(DOCKER_COMPOSE_BIN) -f docker-compose.yml up -d
	@echo "⏳ Очікування запуску сервісів..."
	@sleep 10
	@echo "✅ Всі сервіси запущені!"

# Зупиняє всі контейнери
down:
	@echo "🛑 Зупинка всіх контейнерів..."
	$(DOCKER_COMPOSE_BIN) -f docker-compose.yml down

# Перезапуск усіх контейнерів
restart: down up

# Вивести логи всіх сервісів
logs:
	$(DOCKER_COMPOSE_BIN) -f docker-compose.yml logs -f

# Показати активні контейнери
ps:
	$(DOCKER_COMPOSE_BIN) -f docker-compose.yml ps

# Створення нових міграцій для user-service
makemigrations_user_service: check_venv install_all
	@echo "🛠 Створення нових міграцій для user-service..."
	$(PYTHON_BIN) backend_api/user-service/manage.py makemigrations

# Виконання міграцій для user-service
migrate_user_service: check_venv install_all
	@echo "🔄 Виконання міграцій для user-service..."
	$(PYTHON_BIN) backend_api/user-service/manage.py migrate

# Створення суперкористувача для user-service
super_user_service: check_venv install_all
	@echo "👤 Створення суперкористувача для user-service..."
	$(PYTHON_BIN) backend_api/user-service/manage.py createsuperuser

# Зупинка Django сервера для user-service
kill_user_service: check_venv
	@echo "🛑 Зупинка Django сервера для user-service..."
	@ps aux | grep "python backend_api/user-service/manage.py runserver" | grep -v grep | awk '{print $$2}' | xargs -r kill || echo "Сервер не був запущений."

# Запускає сервер Django для user-service без Docker
run_user_service: check_venv install_all
	@echo "🚀 Запуск Django сервера для user-service..."
	$(PYTHON_BIN) backend_api/user-service/manage.py runserver localhost:8000

# Запускає тести для user-service
test_user_service: check_venv install_all
	@echo "🧪 Запуск тестів Django для user-service..."
	$(PYTHON_BIN) backend_api/user-service/manage.py test app

# Запуск Celery Workers і Beat для user-service
work_user_service: check_venv install_all
	@echo "🚀 Запуск Celery Workers і Beat для user-service локально..."
	@$(PYTHON_BIN) backend_api/user-service/manage.py run_worker --loglevel=INFO -Q default --hostname=user-service-worker@%h & echo $$! > user-service-worker.pid
	@$(PYTHON_BIN) backend_api/user-service/manage.py run_beat --loglevel=INFO & echo $$! > user-service-beat.pid
	@echo "✅ Celery Worker і Beat для user-service запущені у фоновому режимі!"

# Зупинка Celery для user-service
nowork_user_service:
	@echo "🛑 Зупинка Celery для user-service..."
	@if [ -f user-service-worker.pid ]; then kill `cat user-service-worker.pid` && rm user-service-worker.pid && echo "✅ User-service worker зупинено." || echo "User-service worker не був запущений."; fi
	@if [ -f user-service-beat.pid ]; then kill `cat user-service-beat.pid` && rm user-service-beat.pid && echo "✅ User-service beat зупинено." || echo "User-service beat не був запущений."; fi

# Заповнення тестової бази даних для user-service
seed_user_service: check_venv install_all
	@echo "🌱 Заповнення тестової бази даних для user-service..."
	$(PYTHON_BIN) backend_api/user-service/manage.py seed_database --users 10

# Очищення бази даних для user-service
flush_user_service: check_venv install_all
	@echo "🗑 Очищення бази даних для user-service..."
	$(PYTHON_BIN) backend_api/user-service/manage.py flush --noinput