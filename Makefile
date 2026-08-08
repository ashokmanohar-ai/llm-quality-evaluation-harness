.PHONY: install lint test evaluate gate security serve quality e2e

install:
	python -m pip install -e ".[dev]"

lint:
	python -m ruff check src tests scripts

test:
	python -m pytest --cov --cov-report=term-missing --cov-report=xml:reports/coverage.xml

evaluate:
	python -m llm_quality_harness.cli evaluate --dataset datasets/golden.json --output reports/evaluation.json

gate:
	python -m llm_quality_harness.cli gate --results reports/evaluation.json --config config/quality-gates.yaml

security:
	python scripts/secret_scan.py .

serve:
	python -m llm_quality_harness.cli serve

quality: lint test evaluate gate security

e2e:
	npm ci && npx playwright install chromium && npm run test:e2e

