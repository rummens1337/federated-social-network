# Get arguments 
FLASK_SERVER_TYPE = $(type)
FLASK_PORT = $(port)

# Set the default flask port to 5000
ifeq ($(FLASK_PORT),)
FLASK_PORT = 5000
endif

# Set the default flask server type to central
ifeq ($(FLASK_SERVER_TYPE),)
FLASK_SERVER_TYPE = central
endif

# Variables used in dockerfiles
export FLASK_SERVER_TYPE
export FLASK_PORT

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
COMPOSE_PROJECT_NAME=${FLASK_SERVER_TYPE}
export COMPOSE_PROJECT_NAME

# Set data / central different ports
PHPMYADMIN_PORT = 7000
MYSQL_PORT=6000

ifeq (${FLASK_SERVER_TYPE}, DATA)
PHPMYADMIN_PORT = 7001
MYSQL_PORT=6001
endif

ifeq (${FLASK_SERVER_TYPE}, data)
PHPMYADMIN_PORT = 7001
MYSQL_PORT=6001
endif

export MYSQL_PORT
export PHPMYADMIN_PORT

# Starts all docker containers as described in the docker-compose.yml file
run:
	docker-compose -f docker-compose.dev.yml -f docker-compose.yml up --remove-orphans --build

# Starts all docker containers as described in the docker-compose.yml file as production
run-prod:
	docker-compose -f docker-compose.prod.yml -f docker-compose.yml up --remove-orphans --build

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
