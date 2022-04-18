FROM python:3.10-slim-buster

WORKDIR /app

RUN apt-get update && apt-get install curl -y

COPY requirements.txt ./requirements.txt

RUN pip3 install -r requirements.txt

COPY .env ./.env
COPY multiapi .

EXPOSE 80

HEALTHCHECK CMD curl --fail http://localhost:80/health || exit 1

CMD uvicorn --port 80 --host 0.0.0.0 app:app