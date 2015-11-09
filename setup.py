#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import watchman

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = watchman.__version__

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='django-watchman',
    version=version,
    description="""django-watchman exposes a status endpoint for your backing services""",
    long_description=readme + '\n\n' + history,
    author='Michael Warkentin',
    author_email='mwarkentin@gmail.com',
    url='https://github.com/mwarkentin/django-watchman',
    packages=[
        'watchman',
    ],
    include_package_data=True,
    install_requires=[
        'django',
        'django-jsonview==0.5.0',
    ],
    license="BSD",
    zip_safe=False,
    keywords='django-watchman',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
)
