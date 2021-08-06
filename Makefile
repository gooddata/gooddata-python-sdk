all:
	echo "Nothing here yet."

.PHONY: dev
dev:
	python3 -m venv .venv --upgrade-deps
	.venv/bin/pip3 install -r dev-requirements.txt
	pre-commit install

.PHONY: lint
lint:
	flake8 .

.PHONY: format
format:
	black --check .

.PHONY: format-fix
format-fix:
	black .
