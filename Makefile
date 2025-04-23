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
	$(PYTHON_BIN) backend_api/manage.py customcreatesuperuser

kill: ## Зупинка Django сервера
	@echo "🛑 Зупинка Django сервера..."
	@ps aux | grep "python backend_api/manage.py runserver" | grep -v grep | awk '{print $$2}' | xargs -r kill || echo "Сервер не був запущений."

run: check_venv ## Запускає сервер Django без Docker
	@echo "🚀 Запуск Django сервера..."
	$(PYTHON_BIN) backend_api/manage.py runserver localhost:8000

test: check_venv ## Запускає тести Django
	@echo "🧪 Запуск тестів Django..."
	$(PYTHON_BIN) backend_api/manage.py test core

