FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1
ENV PYTHON_VERSION 3.7

RUN apk update && apk -U upgrade
RUN apk add --no-cache \
    openssh-client \
    git \
    libffi-dev \
    postgresql-dev \
    build-base \
    nginx \
    supervisor

RUN pip install --upgrade pip

ADD requirements.txt .
RUN pip install -r requirements.txt && rm requirements.txt

RUN mkdir /app
WORKDIR /app
ADD src /app

RUN mkdir -p /var/run/

# Cleanup packages used while installing PIP packages, but not needed anymore.
RUN apk del \
    openssh-client && \
    rm -rf /var/cache/apk/*

COPY supervisord.conf /etc/supervisor/supervisord.conf

EXPOSE 80
ENTRYPOINT  ["/usr/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf"]
