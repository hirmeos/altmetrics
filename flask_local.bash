#!/bin/bash

# Set env variables for the altmetrics service.
# For convenience, I would recommend creating an alias that run this script. 


# DB Credentials
export DB_USER='altmetrics_user'
export DB_PASSWORD='altmetrics_pw'
export DB_NAME='altmetrics_db'
export DB_HOST='localhost'
export PORT='5432'

# Flask settings for dev - no need to change
export FLASK_APP=core
export FLASK_ENV=development
export CONFIG=DevConfig

# RabbitMQ Credentials
export RMQ_HOST=localhost
export RMQ_VHOST=altmetrics
export RMQ_USER=user
export RMQ_PASSWORD=password 

# RabbitMQ credentials to be used by nameko
export NAMEKO_USER=user
export NAMEKO_PASSWORD=password
export NAMEKO_VHOST=comms

# Security 
export SECURITY_PASSWORD_SALT='very-secure-password-salt'

# Maigun credentials
export MAIL_SERVER='smtp.mailgun.org'
export MAIL_PORT=587
export MAIL_USERNAME='username@mailgun.account'
export MAIL_PASSWORD='mailgun-password'
export MAIL_DEFAULT_SENDER='noreply@hirmeos-altmetrics.com'

# Twitter Dev crentials 
export TWITTER_APP_KEY='twitter-key'
export TWITTER_APP_KEY_SECRET='twitter-key-secret'
export TWITTER_ACCESS_TOKEN='twitter-access-token'
export TWITTER_ACCESS_TOKEN_SECRET='twitter-access-token-secret'
export TWITTER_LABEL=dev


export TECH_EMAIL=demo.user@mail.com

ARGS=("$*")

$ARGS
