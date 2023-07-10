#! /usr/bin/env bash

# Let the DB start
python ./src/app_pre_start.py

# Run migrations
PYTHONPATH=src alembic upgrade head

# Create initial data in DB
python ./src/initial_data.py
