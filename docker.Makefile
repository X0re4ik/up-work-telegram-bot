# Bring up application containers WITHOUT putting them in the background
#                                 -------
up:
	docker-compose -f ./docker-compose.prod.yml --env-file=.docker-compose.prod.env up --build

# Bring up application containers WITH putting them in the background
#                                 ----
detach-up:
	docker-compose -f ./docker-compose.prod.yml --env-file=.docker-compose.prod.env up -d --build

# Forcing all containers to stop
stop:
	docker stop telegram_bot newsletter || true
	docker rm telegram_bot newsletter || true

# Delete service container images
rmi:
	docker system prune --all --force

# Full restsrt (stop -> rmi -> detach-up)
restart:
	make -f docker.Makefile stop &&\
	make -f docker.Makefile rmi && \
	make -f docker.Makefile detach-up
