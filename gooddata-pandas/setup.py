import subprocess
from setuptools import setup, find_packages, Extension

REQUIRES = [
    "gooddata-sdk >= 0.1",
    "pandas"
]

setup(
    name='gooddata-pandas',
    version='0.1',
    author='Lubomir Slivka',
    license='MIT',
    install_requires=REQUIRES,
    packages=['gooddata_pandas']
)
