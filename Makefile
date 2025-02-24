#!/usr/bin/make
# Makefile readme (en): <https://www.gnu.org/software/make/manual/html_node/index.html#SEC_Contents>

docker_bin := $(shell command -v docker 2> /dev/null)
docker_compose_old := $(shell command -v docker_compose 2> /dev/null)
docker_compose_new := $(docker_bin) compose

ifdef docker_compose_old
    docker_compose_bin := $(docker_compose_old)
else
    docker_compose_bin := $(docker_compose_new)
endif

up: ## Start all containers (no interact) for development
    -$(docker_compose_old) up --no-recreate -d || $(docker_compose_new) up --no-recreate -d
down: ## Stop all started for development containers
    -$(docker_compose_old) down || $(docker_compose_new) down