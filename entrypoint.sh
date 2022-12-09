#!/bin/bash

cd /usr/src/app
# docker-compose exec gunicorn python manage.py makemigrations --noinput
# docker-compose exec gunicorn python manage.py migrate --noinput
# docker-compose exec gunicorn python manage.py collectstatic --noinput
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput
gunicorn mysite.wsgi --bind=unix:/var/run/gunicorn/gunicorn.sock