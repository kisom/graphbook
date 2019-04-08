init:
	pip3.7 install -r requirements.txt --user

init_dev: init
	pip3.7 install -r requirements-dev.txt --user

test: check
	py.test tests

check:
	black graphbook --check
	mypy -p graphbook

format:
	black graphbook

doc:
	cd docs && make html

doc_serve:
	cd docs/_build/html && python3.7 -m http.server

doc_watch:
	make doc && ( make doc_serve & ) && cd docs && watch make html

.PHONY: check format init init_dev test doc doc_serve
