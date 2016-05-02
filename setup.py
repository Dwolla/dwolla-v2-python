import os
import sys
import warnings

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='dwollav2',
    version='0.0.1',
    packages=['dwollav2'],
    install_requires=[
        'requests>=2.9.1',
        'future>=0.15.2'
    ],
    test_suite='dwollav2.test.all',
)
