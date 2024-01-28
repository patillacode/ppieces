
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