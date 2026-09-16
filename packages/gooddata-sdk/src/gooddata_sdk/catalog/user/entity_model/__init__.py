# (C) 2022 GoodData Corporation
from gooddata_sdk._lazy import submodule_getattr

# Expose submodules as attributes without importing them eagerly.
__getattr__ = submodule_getattr(__name__)
