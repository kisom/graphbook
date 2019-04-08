PIP ?=	$(shell command -v pip3.7 || command -v pip3)

init:
	$(PIP) install -r requirements.txt --user

init_dev: init
	$(PIP) install -r requirements-dev.txt --user

test: check
	py.test --cov graphbook tests

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

print-%: ; @echo $* is $($*)

.PHONY: check format init init_dev test doc doc_serve
