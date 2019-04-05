init:
	pip3 install -r requirements.txt

test:
	py.test tests

check:
	black graphbook
	mypy -p graphbook

.PHONY: init tets
