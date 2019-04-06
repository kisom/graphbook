init:
	pip3 install -r requirements.txt

init_dev: init
	pip3 install -r requirements-dev.txt

test:
	py.test tests

check:
	black graphbook
	mypy -p graphbook

.PHONY: init tets
