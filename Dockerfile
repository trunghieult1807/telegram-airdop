FROM python:3.11-alpine

RUN apk add --no-cache gcc musl-dev libffi-dev openssl-dev

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install --upgrade pip setuptools wheel
RUN pip3 install --no-warn-script-location --no-cache-dir -r requirements.txt

COPY . /app