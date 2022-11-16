# (C) 2021 GoodData Corporation
from pathlib import Path

from setuptools import find_packages, setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

REQUIRES = [
    "gooddata-afm-client~=1.2.0",
    "gooddata-metadata-client~=1.2.0",
    "gooddata-scan-client~=1.2.0",
    "gooddata-api-client~=1.2.0",
    'importlib-metadata >= 1.0 ; python_version >= "3.7"',
    "python-dateutil>=2.5.3",
    "pyyaml>=5.1",
    "attrs==21.4.0",
    "cattrs==22.1.0",
]


setup(
    name="gooddata-sdk",
    description="GoodData.CN Python SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version="1.2.0",
    author="GoodData",
    author_email="support@gooddata.com",
    license="MIT",
    license_file="LICENSE.txt",
    license_files=("LICENSE.txt",),
    install_requires=REQUIRES,
    packages=find_packages(exclude=["tests*"]),
    python_requires=">=3.7.0",
    project_urls={
        "Documentation": "https://gooddata-sdk.readthedocs.io/en/v1.2.0",
        "Source": "https://github.com/gooddata/gooddata-python-sdk",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
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
