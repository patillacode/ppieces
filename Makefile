test-pypi: test-pypi-release
pypi: pypi-release


# venv/bin/pip install -e .
install:
	python -m venv venv
	venv/bin/pip install --upgrade pip
	venv/bin/pip install -r requirements.txt


test-pypi-release:
	bamp patch
	hatch clean
	hatch build
	hatch publish --repo https://test.pypi.org/legacy/

pypi-release:
	bamp patch
	hatch clean
	hatch build
	hatch publish

bamp-patch:
	bamp patch
	git add --all
	git commit -m "Bump version: $(shell bamp current-version)"

bamp-minor:
	bamp minor
	git add --all
	git commit -m "Bump version: $(shell bamp current-version)"

bamp-major:
	bamp major
	git add --all
	git commit -m "Bump version: $(shell bamp current-version)"
