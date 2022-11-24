from distutils.core import setup

from setuptools import find_packages

setup(
    name='rabbitx',
    version='0.1.0',
    description='Rabbit API client',
    packages=find_packages(exclude=['tests']),
)
