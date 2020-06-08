############################################################
# Dockerfile to build Flask App
# Based on
############################################################

# Set the base image
FROM debian:latest

# File Author / Maintainer
MAINTAINER Carlos Tighe

RUN apt-get update && apt-get install -y apache2 \
    libapache2-mod-wsgi-py3 \
    build-essential \
    python3 \
    python3-dev\
    python3-pip \
    vim \
 && apt-get clean \
 && apt-get autoremove \
 && rm -rf /var/lib/apt/lists/*

# Copy over and install the requirements
COPY ./docker/apache/requirements.txt /var/www/apache-flask/requirements.txt
RUN pip3 install -r /var/www/apache-flask/requirements.txt

# Copy over the apache configuration file and enable the site
COPY ./docker/apache/apache-flask.conf /etc/apache2/sites-available/apache-flask.conf
RUN a2ensite apache-flask
RUN a2enmod headers

# Copy over the wsgi file
COPY ./docker/apache/apache-flask.wsgi /var/www/apache-flask/apache-flask.wsgi

COPY ./run.py /var/www/apache-flask/run.py
COPY ./config.py /var/www/apache-flask/config.py
# COPY $HOST/app /var/www/apache-flask/app/

RUN a2dissite 000-default.conf
RUN a2ensite apache-flask.conf

ARG FLASK_SERVER_TYPE
ENV SERVER_TYPE $FLASK_SERVER_TYPE

EXPOSE 80

WORKDIR /var/www/apache-flask/app

CMD  /usr/sbin/apache2ctl -D FOREGROUND
