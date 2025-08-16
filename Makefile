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

# Встановлення всіх залежностей для user_service
install_user_service: check_venv
	@echo "📦 Встановлення залежностей для user_service..."
	$(PIP_BIN) install --no-cache-dir -r backend_api/user_service/requirements.txt

# Встановлення всіх залежностей для order_service
install_order_service: check_venv
	@echo "📦 Встановлення залежностей для order_service..."
	$(PIP_BIN) install --no-cache-dir -r backend_api/order_service/requirements.txt

# Встановлення всіх залежностей для payment_service
install_payment_service: check_venv
	@echo "📦 Встановлення залежностей для payment_service..."
	$(PIP_BIN) install --no-cache-dir -r backend_api/payment_service/requirements.txt

# Встановлення всіх залежностей
install_all: install_user_service install_order_service install_payment_service
	@echo "📦 Всі залежності встановлено."

# Повний автоматичний запуск усіх контейнерів
up: install_all
	@echo "🚀 Запуск усіх контейнерів..."
	$(DOCKER_COMPOSE_BIN) -f docker-compose.yml up -d
	@echo "⏳ Очікування запуску сервісів..."
	@sleep 30
	@echo "✅ Всі сервіси запущені!"

# Зупиняє всі контейнери
down:
	@echo "🛑 Зупинка всіх контейнерів..."
	$(DOCKER_COMPOSE_BIN) -f docker-compose.yml down

# Перезапуск усіх контейнерів
restart: down up

# Заповнення тестової бази даних для user_service
seed_user_service: check_venv install_user_service
	@echo "🌱 Заповнення тестової бази даних для user_service..."
	$(PYTHON_BIN) backend_api/user_service/manage.py seed_database --users 10

# Заповнення тестової бази даних для order_service
seed_order_service: check_venv install_order_service
	@echo "🌱 Заповнення тестової бази даних для order_service..."
	$(PYTHON_BIN) backend_api/order_service/manage.py seed_database --orders 10

# Заповнення тестової бази даних для payment_service
seed_payment_service: check_venv install_payment_service
	@echo "🌱 Заповнення тестової бази даних для payment_service..."
	$(PYTHON_BIN) backend_api/payment_service/manage.py seed_database --payments 10

# Очищення бази даних для user_service
flush_user_service: check_venv install_user_service
	@echo "🗑 Очищення бази даних для user_service..."
	$(PYTHON_BIN) backend_api/user_service/manage.py flush --noinput

# Очищення бази даних для order_service
flush_order_service: check_venv install_order_service
	@echo "🗑 Очищення бази даних для order_service..."
	$(PYTHON_BIN) backend_api/order_service/manage.py flush --noinput

# Очищення бази даних для payment_service
flush_payment_service: check_venv install_payment_service
	@echo "🗑 Очищення бази даних для payment_service..."
	$(PYTHON_BIN) backend_api/payment_service/manage.py flush --noinput

# Запуск Celery для user_service локально
run_user_service_celery: check_venv install_user_service
	@echo "🚀 Запуск Celery Worker і Beat для user_service локально..."
	@$(PYTHON_BIN) backend_api/user_service/manage.py run_worker --loglevel=INFO -Q default --hostname=user-service-worker@%h & echo $$! > user_service-worker.pid
	@$(PYTHON_BIN) backend_api/user_service/manage.py run_beat --loglevel=INFO & echo $$! > user_service-beat.pid
	@echo "✅ Celery Worker і Beat для user_service запущені у фоновому режимі!"

# Зупинка Celery для user_service
nowork_user_service:
	@echo "🛑 Зупинка Celery для user_service..."
	@if [ -f user_service-worker.pid ]; then kill `cat user_service-worker.pid` && rm user_service-worker.pid && echo "✅ User_service worker зупинено." || echo "User_service worker не був запущений."; fi
	@if [ -f user_service-beat.pid ]; then kill `cat user_service-beat.pid` && rm user_service-beat.pid && echo "✅ User_service beat зупинено." || echo "User_service beat не був запущений."; fi