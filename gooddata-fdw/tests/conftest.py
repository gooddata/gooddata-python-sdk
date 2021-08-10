# (C) 2021 GoodData Corporation
from gooddata_fdw import environment


def pytest_configure(config):
    # This is here to ensure that FDW's environment is aware it runs
    environment._called_from_test = True
