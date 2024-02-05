PYTHON_GLOBAL = python
VENV = venv/bin/
PYTHON = $(VENV)python
PIP = $(VENV)pip
GIT = git

.PHONY: install run

install:
	$(info Creating virtual environment...)
	@$(PYTHON_GLOBAL) -m venv venv
	$(info Upgrading pip...)
	@$(PIP) install --upgrade pip
	$(info Installing requirements...)
	@$(PIP) install -r requirements.txt

run:
	@$(PYTHON) main.py
