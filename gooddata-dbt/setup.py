# (C) 2023 GoodData Corporation
from pathlib import Path

from setuptools import find_packages, setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

REQUIRES = [
    "gooddata-sdk~=1.42.0",
    "pyyaml>=6.0",
    "attrs>=21.4.0,<=24.2.0",
    "cattrs>=22.1.0,<=24.1.1",
    "requests~=2.32.0",
    "tabulate~=0.8.10",
]

setup(
    name="gooddata-dbt",
    description="dbt plugin for GoodData",
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
    python_requires=">=3.9.0",
    scripts=[
        "bin/gooddata-dbt",
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
    keywords=[],
    include_package_data=True,
)
