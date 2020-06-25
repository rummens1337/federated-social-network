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
    ssh-client \
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
COPY ./jwtRS256.key /var/www/apache-flask/jwtRS256.key
COPY ./jwtRS256.key.pub /var/www/apache-flask/jwtRS256.key.pub
COPY ./app/ /var/www/apache-flask/app/
RUN chown -R www-data:www-data /var/www/apache-flask/
RUN chmod -R 755 /var/www/apache-flask/ 
# 775 for upload folders!!

# COPY ./docker/key.sh /var/www/apache-flask/key.sh

RUN a2dissite 000-default.conf
RUN a2ensite apache-flask.conf

ARG FLASK_SERVER_TYPE
ENV FLASK_SERVER_TYPE $FLASK_SERVER_TYPE

ENV FLASK_APP app

EXPOSE 80

WORKDIR /var/www/apache-flask/

RUN pip3 install flask-jwt-extended\[asymmetric_crypto\]

CMD  /usr/sbin/apache2ctl -D FOREGROUND
