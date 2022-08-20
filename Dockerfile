# syntax=docker/dockerfile:1
FROM python:3.9-slim
WORKDIR /Users/nir/Projects/jeeves
COPY requirements.txt ./
COPY . .

ENV PORT=8000
ENV QUART_APP=app:app

RUN pip3 install -r requirements.txt
ENTRYPOINT hypercorn --reload --bind 0.0.0.0:$PORT --workers 1 $QUART_APP
EXPOSE $PORT