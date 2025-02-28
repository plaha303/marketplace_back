#!/usr/bin/make
# Makefile readme (en): <https://www.gnu.org/software/make/manual/html_node/index.html#SEC_Contents>

# Визначаємо Docker залежно від ОС
ifeq ($(OS),Windows_NT)
    DOCKER := docker
    # Шлях до docker-compose для Windows (можна адаптувати)
    DOCKER_COMPOSE := "C:\Program Files\Docker\Docker\resources\bin\docker-compose.exe"
else
    DOCKER := $(shell which docker 2>/dev/null)
    # Спробуємо знайти docker-compose, якщо він є, інакше використовуємо docker compose
    DOCKER_COMPOSE := $(shell which docker-compose 2>/dev/null)
    ifeq ($(DOCKER_COMPOSE),)
        DOCKER_COMPOSE := $(DOCKER) compose
    endif
endif

# Перевіряємо наявність Docker
ifndef DOCKER
    $(error Docker is not installed or not found in PATH)
endif

# Перевіряємо наявність docker-compose або docker compose
ifndef DOCKER_COMPOSE
    $(error Docker Compose is not installed or not found in PATH)
endif

# Ціль для запуску контейнерів
up: ## Start all containers (no interact) for development
	$(DOCKER_COMPOSE) up --no-recreate -d

# Ціль для зупинки контейнерів
down: ## Stop all started for development containers
	$(DOCKER_COMPOSE) down