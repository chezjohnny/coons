# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Johnny Mariéthoz.
#
# Coons is free software; you can redistribute it and/or modify it under the
# terms of the MIT License; see LICENSE file for more details.

"""Blueprint used for loading templates.

The sole purpose of this blueprint is to ensure that Invenio can find the
templates and static files located in the folders of the same names next to
this file.
"""

from flask import Blueprint, render_template
from flask_login import current_user, login_required

blueprint = Blueprint(
    'coons',
    __name__,
    template_folder='templates',
    static_folder='static',
)


@blueprint.route('/u/', defaults={'path': ''})
@blueprint.route('/u/<path:path>')
@login_required
def users(path):
    """Return professional view."""
    return render_template('coons/u.html')
