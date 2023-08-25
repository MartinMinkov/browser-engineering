# Makefile for the Python project

# Set the default task to `help`
.DEFAULT_GOAL := help

# Variables
VENV_NAME?= .venv
PYTHON=${VENV_NAME}/bin/python
PIP=${VENV_NAME}/bin/pip

# By default, it runs `example1.py`. But you can override it with:
# make run-example EXAMPLE=example2
EXAMPLE?=example1

# Targets

## setup: Set up the virtual environment and install dependencies
setup:
	test -d $(VENV_NAME) || python3 -m venv $(VENV_NAME)
	${PIP} install -U pip
	${PIP} install -r requirements.txt

## clean: Delete the virtual environment and any cache
clean:
	rm -rf $(VENV_NAME)
	find -iname "*.pyc" -delete

## run-main: Run the main.py script in browser-engineering
run-main:
	${PYTHON} src/browser-engineering/main.py

## run-example: Run the given example script in examples
run-example:
	${PYTHON} src/examples/$(EXAMPLE).py

## test: Run tests (assuming you're using pytest, but you can change this)
test:
	${PIP} install pytest
	${PYTHON} -m pytest tests/

## lint: Lint the code (assuming you're using flake8 for linting)
lint:
	${PIP} install flake8
	${VENV_NAME}/bin/flake8 src/

## format: Format the code (assuming you're using black for code formatting)
format:
	${PIP} install black
	${VENV_NAME}/bin/black src/

## type-check: Check types using mypy
type-check:
	${PIP} install mypy
	${VENV_NAME}/bin/mypy src/

## help: Display this help message
help:
	@echo "Please use 'make <target>' where <target> is one of"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
