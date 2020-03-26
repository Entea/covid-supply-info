DISTRIBUTOR_DB_NAME ?= distributor
DISTRIBUTOR_DB_USER ?= master
DISTRIBUTOR_DB_PASSWORD ?= 123456
DISTRIBUTOR_DB_PORT ?= 5435
ENVS = DISTRIBUTOR_DB_NAME=${DISTRIBUTOR_DB_NAME} DISTRIBUTOR_DB_USER=${DISTRIBUTOR_DB_USER} DISTRIBUTOR_DB_PASSWORD=${DISTRIBUTOR_DB_PASSWORD} DISTRIBUTOR_DB_PORT=${DISTRIBUTOR_DB_PORT} 

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
	${ENVS} python manage.py runserver

createsuperuser:
	${ENVS} python manage.py createsuperuser

runscript:
	${ENVS} python manage.py runscript ${SCRIPT}
