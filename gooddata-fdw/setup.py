import subprocess
from setuptools import setup, find_packages, Extension

REQUIRES = [
    "gooddata-sdk >= 0.1"
]

setup(
    name='gooddata-fdw',
    version='0.1',
    author='Lubomir Slivka',
    license='MIT',
    install_requires=REQUIRES,
    packages=['gooddata_fdw']
)
