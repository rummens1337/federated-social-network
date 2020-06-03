# Starts all docker containers as described in the docker-compose.yml file
run:
	docker-compose up --remove-orphans

# If a container is built, it won't rebuild the container.
# It also doesn't rebuild any new versions dependencies.
run-fast:
	docker-compose up --no-recreate

# Stop all running containers
stop:
	docker ps -a -q | ( while read ID; do docker stop $$ID; done )

# !! Remove all existing containers: USE WITH CARE !!
rm:
	docker ps -a -q | ( while read ID; do docker rm $$ID; done )

# Check all container statusses
check:
	docker container ls -a -s --no-trunc