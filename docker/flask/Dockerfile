############################################################
# Dockerfile to build Flask App
# Based on
############################################################

# Set the base image
FROM debian:latest

# File Author / Maintainer
MAINTAINER Carlos Tighe

RUN apt-get update && apt-get install -y \
    libapache2-mod-wsgi \
    build-essential \
    python3 \
    python3-dev\
    python3-pip \
    vim \
    ssh-client \
 && apt-get clean \
 && apt-get autoremove \
 && rm -rf /var/lib/apt/lists/*

# Set the flask ENV variables
ENV FLASK_APP app
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_DEBUG 1

# Create the app folder on the Container
RUN mkdir -p /var/www/flask/app/ 

# Copy over and install the requirements
COPY ./docker/flask/requirements.txt /var/www/flask/app/requirements.txt
RUN pip3 install -r /var/www/flask/app/requirements.txt

COPY ./run.py /var/www/flask/run.py
COPY config.py /var/www/flask/config.py

COPY ./jwtRS256.key /var/www/flask/jwtRS256.key
COPY ./jwtRS256.key.pub /var/www/flask/jwtRS256.key.pub

EXPOSE 80

WORKDIR /var/www/flask

ARG FLASK_SERVER_TYPE
ARG FLASK_PORT
ENV FLASK_SERVER_TYPE $FLASK_SERVER_TYPE
ENV FLASK_PORT $FLASK_PORT
ENV FLASK_ENV development

ENV WAIT_VERSION 2.7.2
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/$WAIT_VERSION/wait /wait
RUN chmod +x /wait

RUN pip3 install flask-jwt-extended\[asymmetric_crypto\]

CMD python3 run.py
# CMD ["python3", "run.py", "-s", $TYPE, "-p", $PORT]
