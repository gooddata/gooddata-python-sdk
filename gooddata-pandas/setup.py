# (C) 2021 GoodData Corporation
from setuptools import find_packages, setup

REQUIRES = [
    "gooddata-sdk~=0.6.0",
    "pandas",
    'importlib-metadata >= 1.0 ; python_version < "3.8"',
]


setup(
    name="gooddata-pandas",
    description="GoodData.CN to pandas",
    version="0.6.0",
    author="GoodData",
    license="MIT",
    install_requires=REQUIRES,
    packages=find_packages(exclude=["tests"]),
    python_requires=">=3.7.0",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Database",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development",
        "Typing :: Typed",
    ],
    keywords=[
        "gooddata",
        "pandas",
        "series",
        "data",
        "frame",
        "data_frame",
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
