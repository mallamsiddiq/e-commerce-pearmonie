#!/bin/bash

# Collect static files
echo "Collecting static files"
# python manage.py collectstatic --noinput


# Make migrations
echo "Making Migrations"
python manage.py makemigrations


# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

rm celerybeat.pid


# Start server
echo "Start server"
# python manage.py runserver 0.0.0.0:8000

exec "$@"
