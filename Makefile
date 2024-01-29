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
bamp-patch:
	$(info Setting version (patch)...)
	@$(BAMP) patch
	$(info Adding changes to git...)
	@$(GIT) add --all
	$(info Committing changes...)
	@$(GIT) commit -m "Bump version: $(shell $(BAMP) current-version)"

bamp-minor:
	$(info Setting version (minor)...)
	@$(BAMP) minor
	$(info Adding changes to git...)
	@$(GIT) add --all
	$(info Committing changes...)
	@$(GIT) commit -m "Bump version: $(shell $(BAMP) current-version)"

bamp-major:
	$(info Setting version (major)...)
	@$(BAMP) major
	$(info Adding changes to git...)
	@$(GIT) add --all
	$(info Committing changes...)
	@$(GIT) commit -m "Bump version: $(shell $(BAMP) current-version)"

# Aliases
test-pypi: bamp-patch test-pypi-release
pypi: bamp-patch pypi-release
