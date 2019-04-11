PIP ?=	$(shell command -v pip3.7 || command -v pip3)
PYTHON ?= $(shell command -v python3.7 || command -v python3)
TUI ?= urwid

init:
	$(PIP) install -r requirements.txt --user

init_dev: init
	$(PIP) install -r requirements-dev.txt --user

# Explicitly ignore the UI code, which isn't tested.
test: check
	py.test --cov graphbook.graph --cov graphbook.vm tests

check:
	black graphbook --check --quiet
	mypy -p graphbook

coverage: check
	py.test --cov-report html --cov graphbook.graph --cov graphbook.vm tests

format:
	black --quiet graphbook

doc:
	cd docs && make html

doc_serve:
	cd docs/_build/html && python3.7 -m http.server

doc_watch:
	make doc && ( make doc_serve & ) && cd docs && watch make html

server: check
	$(PYTHON) -m graphbook.ui.server

tui: check
	$(PYTHON) -m graphbook.ui.$(TUI)

print-%: ; @echo $* is $($*)

.PHONY: check format init init_dev test doc doc_serve
