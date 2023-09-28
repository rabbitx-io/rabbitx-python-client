from distutils.core import setup

from setuptools import find_packages

setup(
    name='rabbitx',
    version='0.1.3',
    description='Rabbit API client',
    packages=find_packages(exclude=['tests']),
    install_requires=['requests', 'web3', 'websocket-client', 'rel'],
)
