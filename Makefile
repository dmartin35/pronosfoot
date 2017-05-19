SHELL := /bin/bash
VENV = /Users/dmartin/pyenv/pronosfoot-py36
APP_LIST ?= season


.PHONY: collectstatic run install test ci locale deploy

locale:
	export DJANGO_SETTINGS_MODULE=pronosfoot.settings.dev; \
	export PATH=$PATH:/usr/local/Cellar/gettext/0.19.8.1/bin; \
	source $(VENV)/bin/activate; \
	python manage.py makemessages -l fr --ignore "tools/*"

collectstatic:
	python manage.py collectstatic --noinput

run:
	python manage.py runserver 0.0.0.0:8000

install:
	pip install -r requirements.txt

migrations-check:
	source $(VENV)/bin/activate; \
	python manage.py makemigrations --check --dry-run

#test: migrations-check
#	@coverage run --source=. manage.py test -v2 $(APP_LIST)

#ci: test
#	@coverage report

#deploy: install collectstatic
#	python manage.py compilemessages

