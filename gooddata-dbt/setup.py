# (C) 2023 GoodData Corporation
from setuptools import find_packages, setup

REQUIRES = [
    "gooddata-sdk~=1.7.0",
    "pyyaml>=5.1",
    "attrs==21.4.0",
    "cattrs==22.1.0",
    "requests~=2.31.0",
    "tabulate~=0.8.10",
]

setup(
    name="gooddata-dbt",
    description="dbt plugin for GoodData",
    version="1.7.0",
    author="GoodData",
    license="MIT",
    author_email="support@gooddata.com",
    install_requires=REQUIRES,
    packages=find_packages(exclude=["tests*"]),
    python_requires=">=3.8.0",
    scripts=[
        "bin/gooddata-dbt",
    ],
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
    keywords=[],
    include_package_data=True,
)
