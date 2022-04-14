ifneq (,$(wildcard ./.env))
include .env
export
ENV_FILE_PARAM = --env-file .env

endif

restart-nginx:
    docker-compose exec nginx nginx -s reload

build:
	docker-compose up --build -d --remove-orphans

run-server:
	docker-compose up --build -d --remove-orphans

build-dev-api:
    docker-compose -f docker-compose-dev.yml up -d build api

build-sonarqube:
    docker-compose -f docker-compose-sonarqube.yml up -d --build

build-elasticsearch:
    docker-compose -f docker-compose-elastic-search.yml up -d --build

remove-permission-folder:
    sudo chmod -rwx 755 certbot
remove-permission-folder-2:
    sudo chmod -R a+rwx ./certbot

filebeatlogs:
    tail -f filebeat-20220414.ndjson

unused-image:
    docker image prune -a

up:
	docker-compose up -d

down:
	docker-compose down

show-logs:
	docker-compose logs

migrate:
	docker-compose exec api python3 manage.py migrate

makemigrations:
	docker-compose exec api python3 manage.py makemigrations
stopserver:
    pkill -f runserver


runserver:
	docker-compose -f docker-compose-dev.yml exec api python3 manage.py runserver 8080

superuser:
	docker-compose -f docker-compose-dev.yml exec api python3 manage.py createsuperuser

collectstatic:
	docker-compose exec api python3 manage.py collectstatic --no-input --clear

down-v:
	docker-compose down -v

volume:
	docker-volume inspect estate-src_postgres_data

all-volume:
    docker rm -f $(docker ps -a -q)

winterfun-db:
	docker-compose exec db psql --username=postgres --dbname=dbwinterfun

test:
	docker-compose exec api pytest -p no:warnings --cov=.

test-html:
	docker-compose exec api pytest -p no:warnings --cov=. --cov-report html

flake8:
	docker-compose exec api flake8 .

black-check:
	docker-compose exec api black --check --exclude=migrations .

black-diff:
	docker-compose exec api black --diff --exclude=migrations .

black:
	docker-compose exec api black --exclude=migrations .



