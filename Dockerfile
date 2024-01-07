FROM python:3.11-alpine

WORKDIR /new_app

RUN apk update && apk add --no-cache --virtual bash git gcc g++

RUN python -m pip install --upgrade pip

COPY requirements.txt .

RUN python -m pip install -r requirements.txt

COPY . .
