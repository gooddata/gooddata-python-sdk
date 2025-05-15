# (C) 2024 GoodData Corporation
from pathlib import Path

from setuptools import find_packages, setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

REQUIRES = [
    "dynaconf>=3.1.11,<4.0.0",
    "gooddata-flight-server~=1.42.0",
    "gooddata-sdk~=1.42.0",
    "orjson>=3.9.15,<4.0.0",
    "pyarrow>=16.1.0",
    "structlog>=24.0.0,<25.0.0",
]

setup(
    name="gooddata-flexconnect",
    description="Build your own data source for GoodData Cloud and GoodData Cloud Native.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version="1.42.0",
    author="GoodData",
    author_email="support@gooddata.com",
    license="MIT",
    license_file="LICENSE.txt",
    license_files=("LICENSE.txt",),
    install_requires=REQUIRES,
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    python_requires=">=3.9.0",
    project_urls={
        "Documentation": "https://gooddata-flexconnect.readthedocs.io/en/v1.42.0",
        "Source": "https://github.com/gooddata/gooddata-python-sdk",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Database",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development",
        "Typing :: Typed",
    ],
    keywords=[
        "gooddata",
        "flight",
        "rpc",
        "flight rpc",
        "custom functions",
        "analytics",
        "headless",
        "business",
        "intelligence",
        "headless-bi",
        "cloud",
        "native",
        "semantic",
        "layer",
        "sql",
        "metrics",
    ],
)
