PYTHON = python
PIP = venv/bin/pip
BAMP = bamp
HATCH = hatch
GIT = git

.PHONY: install version test-pypi-release pypi-release bamp-patch bamp-minor bamp-major

# utils
install:
	$(info Creating virtual environment...)
	@$(PYTHON) -m venv venv
	$(info Upgrading pip...)
	@$(PIP) install --upgrade pip
	$(info Installing package in editable mode...)
	@$(PIP) install -e .

version:
	@$(BAMP) current

# PyPi
test-pypi-release:
	$(info Removing old build...)
	@$(HATCH) clean
	$(info Building new version...)
	@$(HATCH) build
	$(info Publishing to test.pypi.org...)
	@$(HATCH) publish --repo https://test.pypi.org/legacy/

pypi-release:
	$(info Removing old build...)
	@$(HATCH) clean
	$(info Building new version...)
	@$(HATCH) build
	$(info Publishing to pypi.org...)
	@$(HATCH) publish

# Bamping
patch:
	$(info Setting version (patch)...)
	@$(BAMP) patch

minor:
	$(info Setting version (minor)...)
	@$(BAMP) minor

major:
	$(info Setting version (major)...)
	@$(BAMP) major

commit-bamp:
	$(info Committing changes...)
	@$(GIT) add bamp.cfg ppieces/__init__.py pyproject.toml
	@$(GIT) commit -m "Bamp version to $(shell $(BAMP) current)"

# Aliases
test-pypi: patch test-pypi-release
pypi: patch pypi-release
