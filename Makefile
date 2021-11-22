all:
	echo "Nothing here yet."

.PHONY: dev
dev:
	python3.9 -m venv .venv --upgrade-deps
	.venv/bin/pip3 install -r dev-requirements.txt
	.venv/bin/pre-commit install

.PHONY: lint
lint:
	flake8 .

.PHONY: format
format:
	black --check .
	isort --check .

.PHONY: format-diff
format-diff:
	black --diff .
	isort --diff .

.PHONY: format-fix
format-fix:
	black .
	isort .

.PHONY: clients
clients: afm-client metadata-client

.PHONY: afm-client
afm-client:
	scripts/generate_afm_client.sh

.PHONY: metadata-client
metadata-client:
	scripts/generate_metadata_client.sh

.PHONY: scan-client
scan-client:
	scripts/generate_scan_client.sh

.PHONY: test
test:
	tox -r -e py39 -c gooddata-sdk/tox.ini
	tox -r -e py39 -c gooddata-pandas/tox.ini
	tox -r -e py39 -c gooddata-fdw/tox.ini
