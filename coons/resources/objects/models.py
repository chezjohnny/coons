# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Johnny Mariéthoz.
#
# Coons is free software; you can redistribute it and/or modify it under the
# terms of the MIT License; see LICENSE file for more details.

"""Objects models."""

from invenio_db import db
from invenio_files_rest.models import Bucket
from invenio_records.models import RecordMetadataBase
from invenio_records_resources.records.models import RecordFileBase
from sqlalchemy_utils.types import UUIDType


class RecordMetadata(db.Model, RecordMetadataBase):
    """Model for Object module metadata."""

    __tablename__ = 'objects'

    bucket_id = db.Column(UUIDType, db.ForeignKey(Bucket.id))
    bucket = db.relationship(Bucket)


class RecordFile(db.Model, RecordFileBase):
    """Model for Object module record files."""

    record_model_cls = RecordMetadata

    __tablename__ = 'objects_files'
