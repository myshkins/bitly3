# syntax=docker/dockerfile:1

FROM python:3.10.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --upgrade -r requirements.txt

COPY . .

