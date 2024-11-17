MANAGE := poetry run python3 manage.py


install:
	poetry install

start-production:
	poetry run gunicorn --daemon -w 5 -b 0.0.0.0:8000 edu_meet_admin_panel.wsgi

stop-production:
	pkill -f 'edu_meet_admin_panel:application'

start:
	${MANAGE} runserver 0.0.0.0:8000

lint:
	poetry run flake8 edu_meet_admin_panel --exclude migrations

shell:
	${MANAGE} shell_plus --bpython

generate-models:
	${MANAGE} inspectdb --database=default > edu_meet_admin_panel/models.py

migrate:
	${MANAGE} makemigrations --check
	${MANAGE} migrate

build:
	generate-models
	migrate

test:
	poetry run python3 manage.py test

#test-coverage:
#	poetry run coverage run manage.py test
#	poetry run coverage report -m --include=task_manager/* --omit=task_manager/settings.py
#	poetry run coverage xml --include=task_manager/* --omit=task_manager/settings.py

#staticfiles:
#	${MANAGE} collectstatic --no-input

load_user:
	python manage.py loaddata admin_users.json
