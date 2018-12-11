#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='nbu-sdk-python',
    version='1.0.4',
    description='NBU (bank.gov.ua) Python SDK',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['requests'],
)
