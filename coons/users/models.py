# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Johnny Mariéthoz.
#
# Coons is free software; you can redistribute it and/or modify it under the
# terms of the MIT License; see LICENSE file for more details.

"""Objects models."""

from invenio_db import db
from sqlalchemy_utils.types import UUIDType


class StickyObjectsMetadata(db.Model):
    """Model for Object module metadata."""

    __tablename__ = 'sticky_objects'

    id = db.Column(db.Integer, primary_key=True)
    objects_ids = db.Column(db.JSON)
