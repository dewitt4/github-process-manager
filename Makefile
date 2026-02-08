.PHONY: help build up down logs shell clean rebuild test

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

build: ## Build Docker image
	docker-compose build

up: ## Start application in development mode
	docker-compose up -d
	@echo "Application started at http://localhost:5000"

up-prod: ## Start application in production mode
	docker-compose -f docker-compose.prod.yml up -d
	@echo "Application started at http://localhost:5000"

down: ## Stop application
	docker-compose down

logs: ## View application logs
	docker-compose logs -f app

shell: ## Access container shell
	docker-compose exec app /bin/bash

clean: ## Stop and remove containers, volumes, and images
	docker-compose down -v
	docker rmi github-process-manager_app 2>/dev/null || true

rebuild: ## Rebuild and restart application
	docker-compose up -d --build
	@echo "Application rebuilt and started at http://localhost:5000"

restart: ## Restart application
	docker-compose restart app

status: ## Show container status
	docker-compose ps

test: ## Run tests (placeholder)
	docker-compose exec app python -m pytest tests/

install: ## Install dependencies locally (non-Docker)
	pip install -r requirements.txt

run-local: ## Run application locally (non-Docker)
	python app.py

setup: ## Initial setup - copy .env.template to .env
	@if [ ! -f .env ]; then \
		cp .env.template .env; \
		echo ".env file created. Please edit it with your API keys."; \
	else \
		echo ".env file already exists."; \
	fi
