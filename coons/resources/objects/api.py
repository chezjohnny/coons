# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Johnny Mariéthoz.
#
# Coons is free software; you can redistribute it and/or modify it under the
# terms of the MIT License; see LICENSE file for more details.

"""Object python API."""

from flask_login import current_user
from invenio_pidstore.models import PIDStatus
from invenio_pidstore.providers.recordid_v2 import RecordIdProviderV2
from invenio_records.dumpers import ElasticsearchDumper, ElasticsearchDumperExt
from invenio_records.extensions import RecordExtension
from invenio_records.systemfields import ConstantField, ModelField
from invenio_records_resources.records.api import FileRecord as FileRecordBase
from invenio_records_resources.records.api import Record as RecordBase
from invenio_records_resources.records.systemfields import FilesField, \
    IndexField, PIDField, PIDStatusCheckField
from werkzeug.local import LocalProxy

from ...proxies import current_coons
from . import models


class AddOwnerExtensionExtension(RecordExtension):
    """Defines the methods needed by an extension."""

    def post_create(self, record):
        """Called before a record is created."""
        print('===========> post create')
        if hasattr(current_user, 'id'):
            record.setdefault('owners', []).append(current_user.id)
        return record


class ElasticsearchDumperObjectsExt(ElasticsearchDumperExt):
    """Interface for Elasticsearch dumper extensions."""

    def dump(self, record, data):
        """Dump the data for indexing.

        Add type and name on the linked objects.
        """
        for obj in data['metadata'].get('objects', []):
            record = self.resolve(obj)
            _type = record['metadata']['type']
            obj['type'] = _type
            name = record['metadata']['name']
            obj['name'] = name

    def resolve(self, obj):
        """Get the object from the $ref link."""
        pid = obj['$ref'].split('/')[-1]
        record_cls = current_coons.resources['obj'].service.record_cls
        record = record_cls.pid.resolve(pid)
        return record

    def load(self, data, record_cls):
        """Load the data.

        Reverse the changes made by the dump method.
        """
        pass


class FileRecord(FileRecordBase):
    """Object record file API."""

    model_cls = models.FileRecordMetadata
    # record_cls = LocalProxy(lambda: RecordWithFile)


class Record(RecordBase):
    """."""

    # Configuration
    model_cls = models.RecordMetadata

    # System fields
    schema = ConstantField(
        '$schema', 'https://coons.io/schemas/objects/object-v1.0.0.json')

    # expires_at = ModelField()
    index = IndexField('objects-object-v1.0.0', search_alias='objects')

    pid = PIDField('id', provider=RecordIdProviderV2)

    # is_published = PIDStatusCheckField(status=PIDStatus.REGISTERED
    # conceptpid = PIDField('conceptid', provider=RecordIdProviderV2)

    dumper = ElasticsearchDumper(extensions=[ElasticsearchDumperObjectsExt()])

    _extensions = [AddOwnerExtensionExtension()]


class RecordWithFile(Record):
    """Object record with file API."""

    files = FilesField(store=False, file_cls=FileRecord)
    bucket_id = ModelField()
    bucket = ModelField(dump=False)
    _extensions = [AddOwnerExtensionExtension()]
