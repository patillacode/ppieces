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

tag:
	$(info Tagging commit...)
	@$(GIT) tag v$(shell $(BAMP) current)

current-branch:
	@$(GIT) rev-parse --abbrev-ref HEAD

push:
	$(info Pushing commit and tag...)
	@$(GIT) push origin $(shell $(GIT) rev-parse --abbrev-ref HEAD)
	@$(GIT) push --tags

version:
	@$(BAMP) current

# PyPi
test-pypi-release:
	$(info Removing old build...)
	rm -rf dist/
	$(info Building new version...)
	python -m build
	$(info Publishing to test.pypi.org...)
	@$(HATCH) publish --repo https://test.pypi.org/legacy/

pypi-release:
	$(info Removing old build...)
	rm -rf dist/
	$(info Building new version...)
	python -m build
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
patch-release: patch commit-bamp tag push pypi-release
minor-release: minor commit-bamp tag push pypi-release
major-release: major commit-bamp tag push pypi-release
