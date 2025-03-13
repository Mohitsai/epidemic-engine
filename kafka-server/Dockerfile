FROM python:3.11.9-alpine3.19

WORKDIR /kafka-app

RUN apk update && \
    apk add --no-cache git

COPY requirements.txt .
RUN pip3 install --no-cache-dir  -r requirements.txt

COPY consumer_producer.py .

CMD ["python3", "consumer_producer.py"]