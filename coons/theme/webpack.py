# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Johnny Mariéthoz.
#
# Coons is free software; you can redistribute it and/or modify it under the
# terms of the MIT License; see LICENSE file for more details.

"""JS/CSS Webpack bundles for theme."""

from invenio_assets.webpack import WebpackThemeBundle

theme = WebpackThemeBundle(
    __name__,
    'assets',
    default='bootstrap3',
    themes={
        'bootstrap3': dict(
            entry={
                'coons-theme': './scss/coons/theme.scss',
                'coons-preview': './js/coons/previewer.js',
            },
            dependencies={},
            aliases={},
        ),
        # 'semantic-ui': dict(
        #     entry={
        #         'coons-preview': './js/coons/previewer.js',
        #     },
        #     dependencies={
        #         # add any additional npm dependencies here...
        #     },
        #     aliases={
        #         '../../theme.config$': 'less/coons/theme.config',
        #     },
        # ),
    }
)
