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

# Встановлення залежностей
install: check_venv
	@echo "📦 Встановлення залежностей з requirements.txt..."
	$(PIP_BIN) install -r backend_api/requirements.txt

up: install ## Повний автоматичний запуск усіх контейнерів
	@echo "🚀 Запуск усіх контейнерів..."
	$(DOCKER_COMPOSE_BIN) -f docker-compose.yml up -d
	@echo "⏳ Очікування запуску сервісів..."
	@sleep 10
	@echo "✅ Всі сервіси запущені!"

down: ## Зупиняє всі контейнери
	@echo "🛑 Зупинка всіх контейнерів..."
	$(DOCKER_COMPOSE_BIN) -f docker-compose.yml down

restart: down up ## Перезапуск усіх контейнерів

logs: ## Вивести логи всіх сервісів
	$(DOCKER_COMPOSE_BIN) -f docker-compose.yml logs -f

ps: ## Показати активні контейнери
	$(DOCKER_COMPOSE_BIN) -f docker-compose.yml ps

makemigrations: check_venv
	@echo "🛠 Створення нових міграцій..."
	$(PYTHON_BIN) backend_api/manage.py makemigrations

migrate: check_venv
	@echo "🔄 Виконання міграцій..."
	$(PYTHON_BIN) backend_api/manage.py migrate

super: ## Створення суперкористувача
	@echo "👤 Створення суперкористувача..."
	$(PYTHON_BIN) backend_api/manage.py createsuperuser

kill: ## Зупинка Django сервера
	@echo "🛑 Зупинка Django сервера..."
	@ps aux | grep "python backend_api/manage.py runserver" | grep -v grep | awk '{print $$2}' | xargs -r kill || echo "Сервер не був запущений."

run: check_venv ## Запускає сервер Django без Docker
	@echo "🚀 Запуск Django сервера..."
	$(PYTHON_BIN) backend_api/manage.py runserver localhost:8000

test: check_venv ## Запускає тести Django
	@echo "🧪 Запуск тестів Django..."
	$(PYTHON_BIN) backend_api/manage.py test core


PYTHON_BIN ?= python3

# Команда для запуску Celery Workers, Beat і Flower
work: check_venv
	@echo "🚀 Запуск Celery Workers (default, emails, images), Beat і Flower локально..."
	@$(PYTHON_BIN) backend_api/manage.py run_worker --loglevel=INFO -Q default --hostname=worker-default@%h & echo $$! > worker-default.pid
	@$(PYTHON_BIN) backend_api/manage.py run_worker --loglevel=INFO -Q emails --hostname=worker-emails@%h & echo $$! > worker-emails.pid
	@$(PYTHON_BIN) backend_api/manage.py run_worker --loglevel=INFO -Q images --hostname=worker-images@%h & echo $$! > worker-images.pid
	@$(PYTHON_BIN) backend_api/manage.py run_beat --loglevel=INFO & echo $$! > beat.pid
	@$(PYTHON_BIN) backend_api/manage.py run_flower & echo $$! > flower.pid
	@echo "✅ Celery Workers (default, emails, images), Beat і Flower запущені у фоновому режимі!"

# Команда для зупинки Celery Workers, Beat і Flower
nowork:
	@echo "🛑 Зупинка Celery..."
	@if [ -f worker-default.pid ]; then kill `cat worker-default.pid` && rm worker-default.pid && echo "✅ Default worker зупинено." || echo "Default worker не був запущений."; fi
	@if [ -f worker-emails.pid ]; then kill `cat worker-emails.pid` && rm worker-emails.pid && echo "✅ Emails worker зупинено." || echo "Emails worker не був запущений."; fi
	@if [ -f worker-images.pid ]; then kill `cat worker-images.pid` && rm worker-images.pid && echo "✅ Image worker зупинено." || echo "Image worker не був запущений."; fi
	@if [ -f beat.pid ]; then kill `cat beat.pid` && rm beat.pid && echo "✅ Beat зупинено." || echo "Beat не був запущений."; fi
	@if [ -f flower.pid ]; then kill `cat flower.pid` && rm flower.pid && echo "✅ Flower зупинено." || echo "Flower не був запущений."; fi

seed: check_venv ## Заповнення тестової бази даних
	@echo "🌱 Заповнення тестової бази даних..."
	$(PYTHON_BIN) backend_api/manage.py seed_database --users 10 --categories 5 --products 20 --min_hits 10 --orders 5 --reviews 10 --favorites 10

flush: check_venv ## Очищення бази даних
	@echo "🗑 Очищення бази даних..."
	$(PYTHON_BIN) backend_api/manage.py flush --noinput