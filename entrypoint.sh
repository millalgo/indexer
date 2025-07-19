#!/bin/bash

# Hardcoded DB connection details
DB_HOST="db"
DB_PORT="5432"
DB_USER="myuser"
DB_NAME="mydb"

# Wait for Postgres to be available
until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER"; do
  echo "Waiting for Postgres at ${DB_HOST}:${DB_PORT}..."
  sleep 1
done

# After DB is ready, apply migrations and collect static files
python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Start Django via Gunicorn
exec gunicorn core.wsgi:application --bind 0.0.0.0:8000
