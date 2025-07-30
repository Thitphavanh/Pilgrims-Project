FROM python:3.10-slim-bullseye

ENV PYTHONBUFFERED 1
#ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

COPY ./requirements-pp.txt /app/
RUN pip install --no-cache-dir -r requirements.txt gunicorn

COPY . /app/

RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "pilgrims.wsgi:application", "--bind", "0.0.0.0:8000"]