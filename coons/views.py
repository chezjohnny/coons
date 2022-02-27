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

api_blueprint = Blueprint(
    'api-coons-ext',
    __name__,
)


@api_blueprint.record_once
def init(state):
    """Init app."""
    app = state.app
    # Register services - cannot be done in extension because
    # Invenio-Records-Resources might not have been initialized.
    registry = app.extensions['invenio-records-resources'].registry
    ext = app.extensions['coons']
    registry.register(
        ext.resources['obj'].service, service_id='objects-service')
    registry.register(
        ext.resources['obj_files'].service, service_id='mock-files-service')
