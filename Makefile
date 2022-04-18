
NAME=multi_api
TAG=0.1.0

install-requirements:
	pip3 install -r requirements.txt

run:
	cd multiapi && uvicorn --reload --host 0.0.0.0 --port 8080 app:app

tests:
	pytest -m "not integration_test"

tests-coverage:
	coverage run -m pytest -m "not integration_test"
	coverage html
	google-chrome htmlcov/index.html

integration-tests:
	pytest -m "integration_test"

docker-build:
	docker build -t "${NAME}:${TAG}" .

docker-run: docker-build
	docker run -it --rm --name api -p 8080:80 multi_api:0.1.0

docker-run-compose: docker-build
	docker-compose up -d api