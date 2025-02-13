# DJANGO CUSTOM USER
This is a custom user model for Django using django rest framework. It is a simple user model that is used to store user information.

## To clone the project
git clone https://github.com/yourusername/django-custom-user.git

## To create a virtual environment
- python -m venv venv
- source venv/bin/activate

## To install the dependencies
- pip install -r requirements.txt

## To migrate the models
- python manage.py makemigrations
- python manage.py migrate

## To create a super user
- python manage.py createsuperuser

## To run the project
- python manage.py runserver

## Url
- http://localhost:8000/admin
- http://localhost:8000/api/auth/

## Environment Variables
- DB_NAME=Your Database Name
- DB_USER=Your Database User
- DB_PASSWORD=Your Database Password
- DB_HOST=Your Database Host
- DB_PORT=Your Database Port
- SECRET_KEY = Your Secret Key
- ALLOWED_HOSTS=127.0.0.1,localhost,localhost:3000,127.0.0.1:8000
- CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
- CSRF_TRUSTED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000




