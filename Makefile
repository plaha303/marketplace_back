#!/usr/bin/make
# Makefile readme (en): <https://www.gnu.org/software/make/manual/html_node/index.html#SEC_Contents>

docker_bin := $(shell command -v docker 2> /dev/null)
docker_compose_bin := $(shell command -v docker-compose 2> /dev/null)

up: ## Start all containers (no interact) for development
	$(docker_compose_bin) up --no-recreate -d

down: ## Stop all started for development containers
	$(docker_compose_bin) down