# (C) 2024 GoodData Corporation
from pathlib import Path

from setuptools import find_packages, setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

REQUIRES = [
    "dynaconf>=3.1.11,<4.0.0",
    "opentelemetry-api>=1.24.0,<=2.0.0",
    "opentelemetry-sdk>=1.24.0,<=2.0.0",
    "orjson>=3.8.5,<4.0.0",
    "prometheus-client~=0.20.0",
    "pyarrow>=16.1.0",
    "readerwriterlock~=1.0.9",
    "structlog>=24.0.0,<25.0.0",
]

setup(
    name="gooddata-flight-server",
    description="Flight RPC server to host custom functions",
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
        "Documentation": "https://gooddata-flight-server.readthedocs.io/en/v1.42.0",
        "Source": "https://github.com/gooddata/gooddata-python-sdk",
    },
    scripts=[
        "bin/gooddata-flight-server",
    ],
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
