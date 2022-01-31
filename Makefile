VERSION = $$(cat VERSION)

# Docker
ENV_FOLDER=./environment
DOCKER_COMPOSE_SETTINGS = --project-name plmomo --env-file .env -f docker-compose-app.yml
DOCKER_COMPOSE_CONTAINER_NAME = plmomo_v${VERSION}

# VENV
VENV_NAME=plmomo
VENV_PATH=$(ENV_FOLDER)/$(VENV_NAME)
VENV_ACTIVATE_PATH=$(VENV_PATH)/bin/activate
REQUIREMENTS_PATH=$(ENV_FOLDER)/requirements.txt


create-env:
	@echo "======================== Creating the project virtual environment ========================" 
	python3 -m virtualenv --system-site-packages -p python3.6 $(VENV_PATH)
	. $(VENV_ACTIVATE_PATH) && \
	python3 -m pip install pip --upgrade && \
	python3 -m pip install -r $(REQUIREMENTS_PATH)

activate-env-command:
	@echo "======================== Execute the below command in terminal ========================" 
	@echo source $(VENV_ACTIVATE_PATH)

docker-build:
	export VERSION=${VERSION} &&\
	docker-compose ${DOCKER_COMPOSE_SETTINGS} build

docker-up:
	export VERSION=${VERSION} &&\
	docker-compose ${DOCKER_COMPOSE_SETTINGS} up -d &&\
	docker exec -it ${DOCKER_COMPOSE_CONTAINER_NAME} python manage.py migrate

docker-down:
	export VERSION=${VERSION} &&\
	docker-compose ${DOCKER_COMPOSE_SETTINGS} down

docker-logs:
	export VERSION=${VERSION} &&\
	docker-compose ${DOCKER_COMPOSE_SETTINGS} logs -f