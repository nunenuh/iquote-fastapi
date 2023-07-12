.PHONY: venv

venv:
	@echo "Activating virtual environment"
	@source venv/bin/activate

run-server:
	PYTHONPATH=src uvicorn main:app --reload --workers 1 --host 0.0.0.0 --port 8000

run-test:
ifdef dst
	PYTHONPATH=src python -m pytest $(dst) -v
else
	PYTHONPATH=src python -m pytest -v
endif


run-test-cov:
	PYTHONPATH=src pytest --cov=src --cov-report=term-missing --cov-report=xml:coverage.xml
	# PYTHONPATH=src coverage report

db-migrate:
	PYTHONPATH=src alembic revision --autogenerate

db-upgrade:
	PYTHONPATH=src alembic upgrade head

run-celery:
	PYTHONPATH=src celery -A src.worker worker -l info -Q default -c 1

precommit:
	pre-commit run --all-files
