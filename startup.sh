#!/bin/bash

cd /mysite
python manage.py makemigrations
python manage.py migrate
gunicorn mysite.wsgi --bind=unix:/var/run/gunicorn/gunicorn.sock