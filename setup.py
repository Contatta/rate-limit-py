#! /usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='rate-limit-py',
    version='0.0.1',
    description='Basic rate limiter using redis',
    url='https://github.com/Contatta/rate-limit-py',
    author='Contatta',
    packages=find_packages('rate_limit'),
    package_data={'rate_limit' : [ '*.lua']},
    include_package_data=True
)

#python setup.py install
#python setup.py develop (to symlink to source)