#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
	name='supermongo',
	version='0.0.0',
	description='Tools to work with Project Dragonfly MongoDB',
	author='Steven Janssens',
	#url='https://github.com/DragonflyTelescope/Dragonfly-AWS',
	packages=find_packages('src'),
	package_dir={'': 'src'},
    install_requires=[
        'pymongo'
    ],
)
