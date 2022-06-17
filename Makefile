all: help

help:
	@echo "To install required packages, run 'make install' from a clean 'python:3.9' (or higher) conda environment."

install:
	pip install -r requirements.txt

lint:
	pylint populare_db_proxy
	pylint tests

test:
	pytest --cov=populare_db_proxy tests
	coverage xml

run:
	# TODO run the proxy

build:
	# TODO build the container--need Dockerfile
