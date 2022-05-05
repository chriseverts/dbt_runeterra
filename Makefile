.PHONY: requirements lint setup build_db

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PROJECT_NAME = runeterra-tracker
PYTHON_INTERPRETER = python3

requirements:
	$(PYTHON_INTERPRETER) -m pip install -U pipenv
	$(PYTHON_INTERPRETER) -m pipenv install --dev

lint:
	pipenv run flake8 src

setup:
	pipenv run pipenv-setup sync --pipfile

build_db:
	pipenv run $(PYTHON_INTERPRETER) explorer/cards_explorer.py
	cd explorer/dbt && pipenv run dbt seed --profiles-dir=. --full-refresh --target=profile_dev
	cd explorer/dbt && pipenv run dbt run --profiles-dir=. --target=profile_dev
