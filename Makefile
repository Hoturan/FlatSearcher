VENV_BIN=.venv/bin

# This makefile has been tested with WSL 2 running with Ubuntu. It should also work with Linux Distros. 

env:
	@echo "Creating a virtual environment in .venv dir..."
	python3 -m venv .venv
	@echo "Activate .venv with source .venv/bin/activate"

upgrade_pip:
	@echo "Updating pip..."
	( \
		. ${VENV_BIN}/activate ; \
		${VENV_BIN}/python -m pip install --upgrade pip ; \
	)

install:
	@echo "Installing dependencies..."
	( \
		. ${VENV_BIN}/activate ; \
		${VENV_BIN}/python -m pip install -r requirements.txt ; \
	)


lint:
	@echo "Testing code style PEP8 and running Linter"
	( \
		. ${VENV_BIN}/activate ; \
		${VENV_BIN}/python -m pylint func_scrape_idealista my_layer --disable=import-error ; \
	)

build:
	@echo "Building lambda function & layers"
	(\
		. ${VENV_BIN}/activate ; \
	    sam build ; \
	)