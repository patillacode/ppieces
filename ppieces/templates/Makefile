PYTHON_GLOBAL = python
VENV = venv/bin/
PYTHON = $(VENV)python
PIP = $(VENV)pip
GIT = git

.PHONY: install run

# utils
create-venv:
	$(info Creating virtual environment...)
	@$(PYTHON) -m venv venv

upgrade-pip:
	$(info Upgrading pip...)
	@$(PIP) install --upgrade pip

install-requirements:
	$(info Installing requirements...)
	@$(PIP) install -r requirements.txt

run:
	@$(PYTHON) main.py


# utils aliases
install: create-venv upgrade-pip install-requirements

