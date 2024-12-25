#!/bin/bash

# Upgrade pip and setuptools
pip install --upgrade pip
pip install --upgrade setuptools

# Install Dependencies
pip install -r requirements.txt

# Run Migrations
python manage.py makemigrations
python manage.py migrate

gunicorn -k uvicorn.workers.UvicornWorker ai_girlfriend.asgi:application

