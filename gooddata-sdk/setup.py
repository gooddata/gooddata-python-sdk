# (C) 2021 GoodData Corporation
from pathlib import Path

from setuptools import find_packages, setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

REQUIRES = [
    "gooddata-api-client~=1.42.0",
    "python-dateutil>=2.5.3",
    "pyyaml>=6.0",
    "attrs>=21.4.0,<=24.2.0",
    "cattrs>=22.1.0,<=24.1.1",
    "brotli==1.1.0",
    "requests~=2.32.0",
    "python-dotenv>=1.0.0,<2.0.0",
]

setup(
    name="gooddata-sdk",
    description="GoodData Cloud Python SDK",
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
    package_data={"gooddata_sdk.cli": ["package.json"]},
    python_requires=">=3.9.0",
    scripts=[
        "bin/gdc",
    ],
    project_urls={
        "Documentation": "https://www.gooddata.com/docs/python-sdk/1.42.0",
        "Source": "https://github.com/gooddata/gooddata-python-sdk",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
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
        "sdk",
        "api",
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
