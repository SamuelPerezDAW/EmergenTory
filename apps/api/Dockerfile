FROM python:3.11.2-slim
WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN django-admin startproject main .
RUN ./manage.py runserver 0.0.0.0:8000
COPY . . 
