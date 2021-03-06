###########################################################################################################
# Setting environmentals
###########################################################################################################

# Get arguments 
FLASK_SERVER_TYPE = $(type)
FLASK_PORT = $(port)
DATA_NUMBER = $(number)
FLASK_DEBUG = $(debug)

$(shell bash key.sh)

# Set the default flask server type to central
ifeq ($(FLASK_SERVER_TYPE),)
FLASK_SERVER_TYPE = central
endif

ifeq ($(DATA_NUMBER),)
DATA_NUMBER = 1
endif

ifeq ($(FLASK_DEBUG),)
FLASK_DEBUG = 0
endif

# Set the default flask port to 5000 if central server
ifeq ($(FLASK_PORT),)
FLASK_PORT = 5000
# and to 9000 if data server
ifeq ($(FLASK_SERVER_TYPE), data)
FLASK_PORT = $(shell expr 9000 + $(DATA_NUMBER))
endif
endif

# Variables used in dockerfiles
export FLASK_SERVER_TYPE
export FLASK_PORT
export DATA_NUMBER

# Check if config is created. If not abort.
ifeq (,$(wildcard config.py))
$(error config.py does not exist. Check installation instructions...)
endif

# Set the mysql data
MYSQL_DATABASE_USER = $(shell echo $(shell sed -n -e "/MYSQL_DATABASE_USER/ s/.*\= *//p" "config.py"))
MYSQL_DATABASE_PASSWORD = $(shell echo $(shell sed -n -e "/MYSQL_DATABASE_PASSWORD/ s/.*\= *//p" "config.py"))
export MYSQL_DATABASE_USER
export MYSQL_DATABASE_PASSWORD

# Set tje project name to data or server so they can both run at the same time
COMPOSE_PROJECT_NAME=${FLASK_SERVER_TYPE}_${DATA_NUMBER}
export COMPOSE_PROJECT_NAME

# Set data / central different ports
PHPMYADMIN_PORT = 7000
MYSQL_PORT=6000

ifeq (${FLASK_SERVER_TYPE}, data)
PHPMYADMIN_PORT = $(shell expr 7000 + $(DATA_NUMBER))
MYSQL_PORT = $(shell expr 6000 + $(DATA_NUMBER))
endif

export MYSQL_PORT
export PHPMYADMIN_PORT

export FLASK_DEBUG

###########################################################################################################
# Commands
###########################################################################################################

# Starts all docker containers as described in the docker-compose.yml file
run:
	docker-compose -f docker-compose.yml up --remove-orphans --build
	pytest

# If a container is built, it won't rebuild the container.
# It also doesn't rebuild any new versions dependencies.
run-fast:
	docker-compose up --no-recreate

reload:
	docker exec -ti apache sh -c "echo a && echo b"

# Stop all running containers
stop:
	docker ps -a -q | ( while read ID; do docker stop $$ID; done )

# !! Stop & Remove all existing containers: USE WITH CARE !!
rm:
	docker ps -a -q | ( while read ID; do docker stop $$ID; done )
	docker ps -a -q | ( while read ID; do docker rm $$ID; done )

# Check all container statusses
check:
	docker container ls -a -s --no-trunc
	
rm-images:
	docker ps -a -q | ( while read ID; do docker stop $$ID; done )
	docker images -a -q | ( while read ID; do docker rmi -f $$ID; done )
