# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Johnny Mariéthoz.
#
# Coons is free software; you can redistribute it and/or modify it under the
# terms of the MIT License; see LICENSE file for more details.

"""Un inventaire à la Prévert"""

import os

from setuptools import find_packages, setup

readme = open('README.rst').read()

packages = find_packages()

# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join('coons', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name='coons',
    version=version,
    description=__doc__,
    long_description=readme,
    keywords='coons Invenio',
    license='MIT',
    author='Johnny Mariéthoz',
    author_email='chezjohnny@gmail.com',
    url='https://github.com/chezjohnny/coons',
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    entry_points={
        'console_scripts': [
            'coons = invenio_app.cli:cli',
        ],
        'invenio_base.apps': [
        ],
        'invenio_base.blueprints': [
            'coons = coons.theme.views:blueprint',
        ],
        'invenio_assets.webpack': [
            'coons_theme = coons.theme.webpack:theme',
            'coons_search_app = coons.records.webpack:search_app',
        ],
        'invenio_config.module': [
            'coons = coons.config',
        ],
        'invenio_i18n.translations': [
            'messages = coons',
        ],
    },
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Development Status :: 3 - Alpha',
    ],
)
