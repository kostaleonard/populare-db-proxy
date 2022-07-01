VERSION=$(shell python -c "from populare_db_proxy import __version__; print(__version__)")

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
	gunicorn --workers 4 --bind 0.0.0.0 'populare_db_proxy.proxy:create_app()'

docker_build:
	@echo Building $(VERSION)
	docker build -t kostaleonard/populare_db_proxy:latest -t kostaleonard/populare_db_proxy:$(VERSION) .

docker_run:
	@echo Running $(VERSION)
	docker run -p 8000:8000 kostaleonard/populare_db_proxy:$(VERSION)

docker_push:
	# TODO
	# TODO add build and push to CD phase
