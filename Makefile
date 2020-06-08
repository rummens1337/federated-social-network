FLASK_SERVER_TYPE = $(type)
FLASK_PORT = $(port)

# FLASK_SERVER_TYPE = ${FLASK_SERVER_TYPE:-CENTRAL}
# FLASK_PORT = ${FLASK_PORT:-5000}

# ifndef FLASK_SERVER_TYPE
# FLASK_SERVER_TYPE = CENTRAL
# endif

# ifndef FLASK_PORT
# FLASK_PORT = 5000
# endif

export FLASK_SERVER_TYPE
export FLASK_PORT

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
