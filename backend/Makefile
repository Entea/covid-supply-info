include .env
export $(shell sed 's/=.*//' .env)

init:
	sudo apt-get install libpq-dev python3-dev
	sudo apt-get install binutils libproj-dev gdal-bin
	python3 -m venv venv

install_deps:
	pip install -r requirements.txt

env-up:
	docker-compose up

end-down:
	docker-compose down

activate:
	source venv/bin/activate

start:
	python manage.py runserver

createsuperuser:
	python manage.py createsuperuser

migrate:
	python manage.py migrate

runscript:
	python manage.py runscript ${SCRIPT}

command:
	python manage.py ${COMMAND}
