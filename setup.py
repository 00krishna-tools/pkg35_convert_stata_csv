#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='pkg35_convert_stata_csv',
    version='0.1.0',
    description="python package to convert files from stata to csv format",
    long_description=readme + '\n\n' + history,
    author="krishna bhogaonker",
    author_email='cyclotomiq@gmail.com',
    url='',
    packages=[
        'pkg35_convert_stata_csv',
    ],
    package_dir={'pkg35_convert_stata_csv':
                 'pkg35_convert_stata_csv'},
    include_package_data=True,
    install_requires=requirements,
    license="ISCL",
    zip_safe=False,
    keywords='pkg35_convert_stata_csv',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
