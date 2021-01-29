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

from flask import Blueprint, jsonify, request
from invenio_db import db

from .models import StickyObjectsMetadata

api_blueprint = Blueprint(
    'sticky_api',
    __name__,
    # prefix='sticky',
    template_folder='templates',
    static_folder='static',
)


@api_blueprint.route('/sticky', methods=['GET', 'PUT'])
def sticky():
    """Sticky API."""
    s = StickyObjectsMetadata.query.first()
    if not s:
        s = StickyObjectsMetadata(objects_ids=[])
        db.session.add(s)
        db.session.commit()
        ids = []
    else:
        ids = s.objects_ids
    if request.method == 'GET':
        return jsonify(ids)

    if request.method == 'PUT':
        s.objects_ids = request.json
        db.session.merge(s)
        db.session.commit()
        return jsonify(s.objects_ids)
