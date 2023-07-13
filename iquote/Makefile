.PHONY: venv

venv:
	@echo "Activating virtual environment"
	@source venv/bin/activate

run-server:
	PYTHONPATH=src uvicorn main:app --reload --workers 1 --host 0.0.0.0 --port 8000

run-test:
ifdef dst
	PYTHONPATH=.:src python -m pytest $(dst) -v
else
	PYTHONPATH=.:src python -m pytest -v
endif


run-test-cov:
	@PYTHONPATH=.:src:$PYTHONPATH pytest --cov=src --cov-report=xml

db-migrate:
	PYTHONPATH=src alembic revision --autogenerate
	PYTHONPATH=src alembic upgrade head

db-upgrade:
	PYTHONPATH=src alembic upgrade head

db-prestart:
	PYTHONPATH=src python ./src/app_pre_start.py
	PYTHONPATH=src alembic upgrade head
	PYTHONPATH=src python ./src/initial_data.py

db-init:
	PYTHONPATH=src alembic init migrations
	PYTHONPATH=src alembic revision --autogenerate

run-celery:
	PYTHONPATH=src celery -A src.worker worker -l info -Q default -c 1

precommit:
	pre-commit run --all-files
