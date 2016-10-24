import os
import sys
import warnings

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='dwollav2',
    version='1.1.8',
    packages=['dwollav2'],
    install_requires=[
        'requests>=2.9.1',
        'future>=0.15.2'
    ],
    test_suite='dwollav2.test.all',
    url='https://docsv2.dwolla.com',
    license='MIT',
    author='Stephen Ausman',
    author_email='stephen@dwolla.com',
    long_description=open('README.md').read(),
    description='Official Dwolla V2 API client',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)
