#!/usr/bin/env python3

import os
import sys

import setuptools

if sys.version_info < (3,):
    raise RuntimeError('Python3 required.')

HERE = os.path.dirname(os.path.realpath(__file__))
VERSION_PY = os.path.join(HERE, 'rule30', 'version.py')
with open(VERSION_PY) as fp:
    exec(fp.read())

setuptools.setup(
    name='rule30',
    version=__version__,
    description='Implementation of Stephen Wolfram\'s elementary cellular automata',
    long_description='See `README <https://github.com/zmwangx/rule30#readme>`_.',
    url='https://github.com/zmwangx/rule30',
    author='Zhiming Wang',
    author_email='zmwangx@gmail.com',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Visualization',
    ],
    keywords='elementary cellular automaton',
    packages=['rule30'],
    install_requires=[
        'Pillow>=4.0.0',
        'bitarray>=0.8.1',
    ],
    extras_require={
        'doc': [
            'Sphinx>=1.5.2',
            'sphinx-rtd-theme>=0.1.9',
        ],
    },
    entry_points={
        'console_scripts': [
            'rule30=rule30.cli:main',
        ]
    },
)
