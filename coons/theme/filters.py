# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Johnny Mariéthoz.
#
# Coons is free software; you can redistribute it and/or modify it under the
# terms of the MIT License; see LICENSE file for more details.

"""Jinja filters."""

import glob
import os
import re

from flask import current_app
from markupsafe import Markup


def node_assets(package, patterns=[
        'runtime*.js', 'polyfills*.js', 'main*.js'], _type='js', tags=''):
    """Generate the node assets html code.

    :param package: The node package path relative to node_modules.
    :param patters: list of glob bash like partterns.
    "param _type: string one of ['js', 'css'].
    "param tags: additional script, link, html tags such as 'defer', etc.
    "return" html link, script code
    """
    package_path = os.path.join(
        current_app.static_folder, 'node_modules', package)

    def to_html(value):
        value = re.sub(r'(.*?)\/static', '/static', value)
        # default: js
        html_code = '<script {tags} src="{value}"></script>'
        # styles
        if _type == 'css':
            html_code = '<link {tags} href="{value}" rel="stylesheet">'
        return html_code.format(
                value=value,
                tags=tags
            )
    output_files = []
    for pattern in patterns:
        files = glob.glob(os.path.join(package_path, pattern))
        output_files.extend([to_html(v) for v in files])

    class HTMLSafe:
        def __html__():
            return Markup('\n'.join(output_files))
    return HTMLSafe
