



SET_PYTHONPATH_TO_STR:
	export PYTHONPATH="$PYTHONPATH:$PWD"

pip-requirements:
	pip install -r requirements.txt

pip-freeze:
	pip freeze -l > requirements.txt


dev-services:
	docker-compose -f ./docker/docker-compose.dev.yml up -d --build