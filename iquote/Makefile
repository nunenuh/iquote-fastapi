
run-server:
	PYTHONPATH=app uvicorn app.main:app --reload --workers 1 --host 0.0.0.0 --port 8000

run-test:
ifdef dst
	PYTHONPATH=app python -m pytest $(dst) -v
else
	PYTHONPATH=app python -m pytest -v
endif


run-test-cov:
	PYTHONPATH=app pytest --cov=app --cov-report=term-missing

db-migrate:
	PYTHONPATH=app alembic revision --autogenerate

db-upgrade:
	PYTHONPATH=app alembic upgrade head

run-celery:
	PYTHONPATH=app celery -A app.worker worker -l info -Q default -c 1

precommit:
	pre-commit run --all-files
