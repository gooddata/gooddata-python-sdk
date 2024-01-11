# (C) 2021 GoodData Corporation
from pathlib import Path

from setuptools import find_packages, setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

REQUIRES = [
    "gooddata-sdk~=1.12.0",
    #    "multicorn>=1.4.0",
]

setup(
    name="gooddata-fdw",
    description="GoodData Cloud Foreign Data Wrapper For PostgreSQL",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version="1.12.0",
    author="GoodData",
    author_email="support@gooddata.com",
    license="MIT",
    license_file="LICENSE.txt",
    license_files=("LICENSE.txt",),
    install_requires=REQUIRES,
    packages=find_packages(exclude=["tests*"]),
    python_requires=">=3.8.0",
    project_urls={
        "Documentation": "https://gooddata-fdw.readthedocs.io/en/v1.12.0",
        "Source": "https://github.com/gooddata/gooddata-python-sdk",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Database",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development",
        "Typing :: Typed",
    ],
    keywords=[
        "gooddata",
        "fdw",
        "postgresql",
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
