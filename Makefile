.PHONY: up down

DOCKER := docker
DOCKER_COMPOSE := $(DOCKER) compose

up: ## Start all containers (no interact) for development
	$(DOCKER_COMPOSE) up --no-recreate -d

down: ## Stop all started for development containers
	$(DOCKER_COMPOSE) down