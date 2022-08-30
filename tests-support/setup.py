# (C) 2022 GoodData Corporation

from setuptools import find_packages, setup

REQUIRES = [
    "pyyaml>=5.1",
]

setup(
    name="tests-support",
    description="Tests support for GoodData Python SDK",
    install_requires=REQUIRES,
    packages=find_packages(exclude=["tests"]),
    python_requires=">=3.7.0",
)
