ENV_FOLDER=./environment
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