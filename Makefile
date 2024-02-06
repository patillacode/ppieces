PYTHON = python
PIP = venv/bin/pip
BAMP = bamp
HATCH = hatch
GIT = git

.PHONY: install version test-pypi-release pypi-release bamp-patch bamp-minor bamp-major

# utils
create-venv:
	$(info Creating virtual environment...)
	@$(PYTHON) -m venv venv

upgrade-pip:
	$(info Upgrading pip...)
	@$(PIP) install --upgrade pip

install-package:
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

# utils aliases
install: create-venv upgrade-pip dev-requirements install-package
re-install: upgrade-pip dev-requirements install-package

# requirements
build-dev-requirements:
	$(info Building development requirements...)
	@$(VENV)pip-compile requirements/development.in -o requirements/development.txt

build-production-requirements:
	$(info Building production requirements...)
	@$(VENV)pip-compile requirements/base.in -o requirements/production.txt

build-test-requirements:
	$(info Building test requirements...)
	@$(VENV)pip-compile requirements/test.in -o requirements/test.txt

install-development-requirements:
	$(info Installing development requirements...)
	@$(PIP) install -r requirements/development.txt

install-production-requirements:
	$(info Installing production requirements...)
	@$(PIP) install -r requirements/development.txt

install-test-requirements:
	$(info Installing test requirements...)
	@$(PIP) install -r requirements/test.txt

delete-requirements-txt:
	$(info Resetting requirements...)
	@rm -f requirements/*.txt

reset-requirements: delete-requirements-txt build-requirements

# requirements aliases
build-requirements: build-dev-requirements build-production-requirements build-test-requirements
dev-requirements: build-dev-requirements install-development-requirements install-package
prod-requirements: build-production-requirements install-production-requirements install-package
test-requirements: build-test-requirements install-test-requirements install-package

# tests
coverage-report:
	coverage run -m pytest -x
	coverage json -o "coverage-summary.json"
	coverage report -m

test:
	pytest -x

# tests aliases
cov: coverage-report

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

# bamping aliases
patch-release: patch commit-bamp tag push pypi-release
minor-release: minor commit-bamp tag push pypi-release
major-release: major commit-bamp tag push pypi-release
