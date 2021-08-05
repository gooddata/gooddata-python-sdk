import subprocess
from setuptools import setup, find_packages, Extension

REQUIRES = [
    "gooddata-afm-client >= 1.0",
    "gooddata-metadata-client >= 1.0"
]

setup(
    name='gooddata-sdk',
    version='0.1',
    author='Lubomir Slivka',
    license='MIT',
    install_requires=REQUIRES,
    packages=['gooddata_sdk']
)
