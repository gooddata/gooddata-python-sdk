from setuptools import setup, find_packages

REQUIRES = [
    "gooddata-afm-client>=1.0.0, <2.0.0",
    "gooddata-metadata-client>=1.0.0, <2.0.0"
]


def _read_version():
    with open('VERSION', 'rt') as version_file:
        return version_file.readline().strip()


setup(
    name='gooddata-sdk',
    version=_read_version(),
    author='GoodData',
    license='MIT',
    install_requires=REQUIRES,
    packages=find_packages(exclude=['tests']),
)
