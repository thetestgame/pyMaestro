"""
Copyright (c) Jordan Maxwell. All rights reserved.
See LICENSE file in the project root for full license information.
"""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

long_description = """
Module for controlling Pololu Maestro board
"""

setup(
    name='pyMaestro',
    description="Module for controlling Pololu Maestro board",
    long_description=long_description,
    license='MIT',
    version='1.0.0',
    author='Jordan Maxwell',
    maintainer='Jordan Maxwell',
    url='https://github.com/thetestgame/pyMaestro',
    packages=['maestro'],
    classifiers=[
        'Programming Language :: Python :: 3',
    ])