PYTHON_GLOBAL = python
VENV = venv/bin/
PYTHON = $(VENV)python
PIP = $(VENV)pip
GIT = git

.PHONY: install run

# utils aliases
install: create-venv upgrade-pip install-requirements

# utils
run:
	@$(PYTHON) main.py

create-venv:
	$(info Creating virtual environment...)
	@$(PYTHON) -m venv venv

upgrade-pip:
	$(info Upgrading pip...)
	@$(PIP) install --upgrade pip
