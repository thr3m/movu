#!/bin/bash

# Wait for the database to be ready
until nc -z movu-db-dev 5432; do
  echo "Waiting for PostgreSQL to become available on port 5432..."
  sleep 2
done

echo "Database is ready!"

python manage.py collectstatic --noinput && 
python manage.py makemigrations && 
python manage.py migrate && 
python manage.py runscript init_data &&
python3 -m gunicorn config.wsgi:application -c gunicorn.cfg.py