#!/bin/bash

python manage.py makemigrations
python manage.py migrate

python create_super_user.py 

# Inicia o servidor Django
python manage.py runserver 0.0.0.0:8000
