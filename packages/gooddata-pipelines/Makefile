# (C) 2025 GoodData Corporation

# Skip tests if running Python 3.9 from CI (gooddata-pipelines doesn't support py39)
ifeq ($(TEST_ENVS),py39)
.PHONY: test-ci
test-ci:
	@echo "Skipping tests for Python 3.9 - gooddata-pipelines doesn't support this version"
	@exit 0

.PHONY: test
test:
	@echo "Skipping tests for Python 3.9 - gooddata-pipelines doesn't support this version"
	@exit 0
else
include ../project_common.mk
endif
