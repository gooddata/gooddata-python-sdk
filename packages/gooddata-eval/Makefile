# (C) 2026 GoodData Corporation
include ../../project_common.mk

.PHONY: calibrate-takeaway
calibrate-takeaway:
	uv run --package gooddata-eval --extra llm-judge python scripts/calibrate_takeaway_judge.py

.PHONY: calibrate-catalog-metadata
calibrate-catalog-metadata:
	uv run --package gooddata-eval --extra llm-judge python scripts/calibrate_catalog_metadata_judge.py
