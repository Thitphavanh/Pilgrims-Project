# Dockerfile
FROM python:3.10-slim-bullseye

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Install postgresql-client for database connectivity and management
RUN apt-get update && apt-get install -y postgresql-client gettext

WORKDIR /app

COPY ./requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# The static root is now 'staticfiles' as defined in base.py
RUN python manage.py collectstatic --noinput --settings=config.settings.prod

# EXPOSE 8000 is not strictly needed but good practice
EXPOSE 8000

# Gunicorn is for production, so we point to production settings
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]