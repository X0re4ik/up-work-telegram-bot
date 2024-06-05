



SET_PYTHONPATH_TO_STR:
	export PYTHONPATH="$PYTHONPATH:$PWD"


global-isort:
	isort .

services-up:
	docker-compose -f ./docker/docker-compose.dev.yml --env-file=./docker/docker-compose.dev.env up -d --build

pip-requirements:
	pip install -r requirements.txt

pip-freeze:
	pip freeze -l > requirements.txt


# to-head:
#     alembic upgrade heads

# autogenerate:
#     alembic revision --autogenerate -m "Init"


# up:
#     docker-compose -f ./docker-compose.prod.yml --env-file=./.docker-compose.prod.env up -d --build
