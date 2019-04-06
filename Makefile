init:
	pip3 install -r requirements.txt

init_dev: init
	pip3 install -r requirements-dev.txt

test: check
	py.test tests

check:
	black graphbook --check
	mypy -p graphbook

format:
	black graphbook

.PHONY: check format init init_dev test
