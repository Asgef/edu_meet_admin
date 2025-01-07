MANAGE := poetry run python manage.py


install:
	poetry install

start-production:
	poetry run gunicorn --daemon -w 5 -b 0.0.0.0:8000 edu_meet_admin_panel.wsgi

stop-production:
	pkill -f gunicorn

start:
	${MANAGE} runserver 0.0.0.0:8000

lint:
	poetry run flake8 .

shell:
	${MANAGE} shell_plus --bpython

generate-models:
	${MANAGE} inspectdb --database=default > edu_meet_admin_panel/models.py

migrate:
	${MANAGE} makemigrations --check
	${MANAGE} migrate

dependencies:
	npm install
	npm run build


build:
	make dependencies
	make staticfiles
	make generate-models
	make migrate

test:
	poetry run python3 manage.py test

#test-coverage:
#	poetry run coverage run manage.py test
#	poetry run coverage report -m --include=task_manager/* --omit=task_manager/settings.py
#	poetry run coverage xml --include=task_manager/* --omit=task_manager/settings.py

staticfiles:
	${MANAGE} collectstatic --no-input

load_user:
	python manage.py loaddata admin_users.json

generate_slots:
	python manage.py init_slots

remove_slots:
	python manage.py delete_unused_slots
