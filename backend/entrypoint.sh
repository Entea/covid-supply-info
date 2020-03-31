#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z $DISTRIBUTOR_DB_HOST $DISTRIBUTOR_DB_PORT; do
  sleep 0.1
done

echo "PostgreSQL started"

python manage.py migrate
python manage.py collectstatic --no-input
python manage.py runserver 0.0.0.0:8000

exec "$@"