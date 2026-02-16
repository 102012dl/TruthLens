# TruthLens Makefile
# ==================
# Author: 102012dl
# Usage: make <target>

.PHONY: help install dev test lint security build deploy clean

# Default target
help:
	@echo "TruthLens - Available commands:"
	@echo ""
	@echo "  make install     - Install all dependencies"
	@echo "  make dev         - Run development server"
	@echo "  make test        - Run all tests"
	@echo "  make lint        - Run linters"
	@echo "  make security    - Run security checks"
	@echo "  make build       - Build Docker images"
	@echo "  make deploy      - Deploy to production"
	@echo "  make clean       - Clean up"
	@echo ""

# ===== Installation =====
install:
	@echo "📦 Installing dependencies..."
	python -m pip install --upgrade pip
	pip install -r requirements.txt
	python -m spacy download en_core_web_sm
	@echo "✅ Installation complete!"

install-dev: install
	pip install -r requirements-dev.txt
	pre-commit install

# ===== Development =====
dev:
	@echo "🚀 Starting development server..."
	uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

dev-bot:
	@echo "🤖 Starting Telegram bot..."
	python -m src.bot.main

dev-web:
	@echo "🌐 Starting web dashboard..."
	cd web && npm run dev

# ===== Database =====
db-migrate:
	@echo "📊 Running database migrations..."
	alembic upgrade head

db-rollback:
	@echo "⏪ Rolling back last migration..."
	alembic downgrade -1

db-seed:
	@echo "🌱 Seeding database..."
	python scripts/seed.py

# ===== Testing =====
test:
	@echo "🧪 Running tests..."
	pytest tests/ -v

test-cov:
	@echo "📊 Running tests with coverage..."
	pytest tests/ --cov=src --cov-report=html --cov-report=term-missing

test-unit:
	pytest tests/unit/ -v

test-integration:
	pytest tests/integration/ -v

# ===== Linting =====
lint:
	@echo "🔍 Running linters..."
	black src/ tests/
	isort src/ tests/
	flake8 src/ tests/ --max-line-length=120

mypy:
	@echo "🔎 Running type checker..."
	mypy src/ --ignore-missing-imports

# ===== Security =====
security:
	@echo "🔒 Running security checks..."
	bandit -r src/ -f txt
	safety check -r requirements.txt

security-full:
	@echo "🔒 Running full security audit..."
	bandit -r src/ -f json -o reports/bandit-report.json
	safety check -r requirements.txt --full-report
	pip-audit

# ===== Docker =====
build:
	@echo "🐳 Building Docker images..."
	docker-compose build

build-prod:
	docker-compose -f docker-compose.prod.yml build

up:
	@echo "🚀 Starting all services..."
	docker-compose up -d

down:
	@echo "🛑 Stopping all services..."
	docker-compose down

logs:
	docker-compose logs -f

# ===== MLOps =====
mlflow:
	@echo "📈 Starting MLflow..."
	mlflow ui --host 0.0.0.0 --port 5000

train:
	@echo "🧠 Training models..."
	python scripts/train.py

# ===== Deployment =====
deploy-staging:
	@echo "🚀 Deploying to staging..."
	./scripts/deploy.sh staging

deploy-prod:
	@echo "🌐 Deploying to production..."
	./scripts/deploy.sh production

# ===== Cleanup =====
clean:
	@echo "🧹 Cleaning up..."
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf htmlcov/ .coverage coverage.xml 2>/dev/null || true
	@echo "✅ Cleanup complete!"
