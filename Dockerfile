FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED 1

WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY requirements.txt /app

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app

ENTRYPOINT ["sh","scripts/docker-entrypoint-dev.sh"]
