FROM python:3.11-slim-bullseye
COPY ./requirements.txt /storage/
WORKDIR /storage
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install --no-install-recommends -y libpq-dev && apt-get clean && rm -rf /var/lib/apt/lists/* && pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
ENTRYPOINT [ "/usr/local/bin/python3", "manage.py", "runserver", "0.0.0.0:8000" ]