FROM python:3.10-slim-bullseye

ENV PYTHONBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app
COPY . ./app/

COPY ./requirements.txt .
RUN pip install -r requirements.txt