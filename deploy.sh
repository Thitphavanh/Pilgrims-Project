python manage.py makemigrations --no-input
python manage.py migrate --no-input

gunicorn pilgrims.wsgi.application --bind 0.0.0.0:8000