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
 && apt-get clean \
 && apt-get autoremove \
 && rm -rf /var/lib/apt/lists/*

# Set the flask ENV variables
ENV FLASK_APP run.py
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_DEBUG 1

# Create the app folder on the Container
RUN mkdir -p /var/www/flask/app/ 

# Copy over and install the requirements
COPY ./docker/flask/requirements.txt /var/www/flask/app/requirements.txt
RUN pip3 install -r /var/www/flask/app/requirements.txt

COPY ./run.py /var/www/flask/run.py
COPY config.py /var/www/flask/config.py
# COPY $HOST/app /var/www/apache-flask/app/

EXPOSE 80

WORKDIR /var/www/flask

ARG FLASK_SERVER_TYPE
ARG FLASK_PORT
ENV SERVER_TYPE $FLASK_SERVER_TYPE
ENV PORT $FLASK_PORT

CMD python3 run.py 
# CMD ["python3", "run.py", "-s", $TYPE, "-p", $PORT]