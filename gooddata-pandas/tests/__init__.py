# (C) 2021 GoodData Corporation
from __future__ import annotations

from dotenv import dotenv_values, find_dotenv


def _load_test_env():
    try:
        test_env = find_dotenv(".env.test", raise_error_if_not_found=True)

        return dotenv_values(test_env)
    except OSError:
        return dict()


def get_test_token():
    config = _load_test_env()

    if "TEST_TOKEN" not in config:
        # returning bogus token so that tests that use vcr recordings have something to use
        return "test-token-undefined"

    return config["TEST_TOKEN"]


TEST_DATA_REGIONS = [
    "Aargau",
    "Basel-Landschaft",
    "Basel-Stadt",
    "Bern",
    "Fribourg",
    "Geneva",
    "Glarus",
    "Graubünden",
    "Jura",
    "Lucerne",
    "Neuchâtel",
    "Nidwalden",
    "Obwalden",
    "Schaffhausen",
    "Schwyz",
    "Solothurn",
    "St. Gallen",
    "Thurgau",
    "Ticino",
    "Uri",
    "Valais",
    "Vaud",
    "Zug",
    "Zürich",
]
