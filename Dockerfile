FROM python:3.10-slim-buster

WORKDIR /app

COPY requirements.txt ./requirements.txt

RUN pip3 install -r requirements.txt

COPY .env ./.env
COPY multiapi .

EXPOSE 8080

HEALTHCHECK CMD curl --fail http://localhost:8080/health || exit 1

CMD uvicorn --port 8080 app:app