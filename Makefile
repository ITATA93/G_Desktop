# Makefile — G_Desktop
# Targets for TypeScript build/lint, Python lint/test, and project maintenance.

.PHONY: help install build lint type-check test clean dev validate backup audit health

# Default target
help: ## Show this help message
	@echo ""
	@echo "  G_Desktop — Available targets"
	@echo "  =============================="
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  %-18s %s\n", $$1, $$2}'
	@echo ""

# --- Setup ---

install: ## Install all dependencies (npm + pip)
	npm install
	pip install -r requirements-dev.txt

# --- TypeScript ---

build: ## Compile TypeScript to dist/
	npx tsc

dev: ## Run development server with hot reload
	npx tsx watch src/index.ts

lint: ## Run ESLint on TypeScript sources
	npx eslint src --ext .ts

type-check: ## Run TypeScript type checking (no emit)
	npx tsc -p tsconfig.check.json

# --- Python ---

lint-py: ## Run Python linter (ruff or flake8)
	python -m ruff check scripts/ tests/ || python -m flake8 scripts/ tests/

test: ## Run all tests (vitest + pytest)
	npx vitest run
	python -m pytest tests/ -v

test-ts: ## Run TypeScript tests only (vitest)
	npx vitest run

test-py: ## Run Python tests only (pytest)
	python -m pytest tests/ -v

# --- Validation ---

validate: ## Validate manifest and type-check
	npx tsx scripts/validate-manifest.ts
	npx tsc -p tsconfig.check.json

audit: ## Run ecosystem normalization audit
	python scripts/audit_ecosystem.py

health: ## Run agent health check
	python scripts/agent_health_check.py

# --- Maintenance ---

backup: ## Backup Notion databases to reports/backups/
	npx tsx scripts/backup-notion.ts

clean: ## Remove build artifacts and caches
	rm -rf dist/
	rm -rf scripts/__pycache__/
	rm -rf tests/__pycache__/
	rm -rf .pytest_cache/
	rm -rf node_modules/.cache/

# --- Sync & Knowledge ---

sync-knowledge: ## Sync knowledge and generate context snapshot
	python scripts/knowledge_sync.py

sync-memory: ## Generate ecosystem status dashboard
	python scripts/memory_sync.py full

sync-templates: ## Check template drift across projects
	python scripts/propagate.py status
