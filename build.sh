#!/bin/bash

# Upgrade pip and setuptools
pip install --upgrade pip
pip install --upgrade setuptools

# Install Dependencies
pip install -r Requriements.txt

# Run Migrations
python manage.py makemigrations
python manage.py migrate


