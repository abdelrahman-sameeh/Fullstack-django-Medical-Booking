#!/bin/bash

python3 manage.py makemigrations 
python3 manage.py makemigrations authentication
python3 manage.py makemigrations medical

python3 manage.py migrate

