
NAME=multi_api
TAG=0.1.0

install-requirements:
	pip3 install -r requirements.txt

run:
	cd multiapi && uvicorn --workers 9 --host 0.0.0.0 --port 8080 app:app  # workers = 2 * number_of_cores + 1

tests:
	pytest -m "not integration_test"

tests-coverage:
	coverage run -m pytest -m "not integration_test"
	coverage html
	google-chrome htmlcov/index.html

integration-tests:
	pytest -m "integration_test"

load-tests:
	locust -f test/test_load  # This test is a manual one

docker-build:
	docker build -t "${NAME}:${TAG}" .

docker-run: docker-build
	docker run --rm --name api -p 8080:80 multi_api:0.1.0

docker-run-compose: docker-build
	docker-compose up -d api