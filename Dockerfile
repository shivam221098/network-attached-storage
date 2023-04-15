FROM python:3.10-slim-buster
RUN mkdir "storage"
COPY . /storage
WORKDIR /storage
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apt-get update
RUN apt-get install -y libpq-dev
RUN apt-get install -y python3-pip
RUN pip install -r requirements.txt
