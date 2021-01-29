# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Johnny Mariéthoz.
#
# Coons is free software; you can redistribute it and/or modify it under the
# terms of the MIT License; see LICENSE file for more details.

"""Object python API."""

from invenio_pidstore.models import PIDStatus
from invenio_pidstore.providers.recordid_v2 import RecordIdProviderV2
from invenio_records.dumpers import ElasticsearchDumper, ElasticsearchDumperExt
from invenio_records.systemfields import ConstantField, ModelField
from invenio_records_resources.records.api import Record as RecordBase
from invenio_records_resources.records.api import RecordFile as RecordFileBase
from invenio_records_resources.records.systemfields import FilesField, \
    IndexField, PIDField, PIDStatusCheckField
from werkzeug.local import LocalProxy

from ...proxies import current_coons
from . import models


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


class RecordFile(RecordFileBase):
    """Object record file API."""

    model_cls = models.RecordFile
    record_cls = LocalProxy(lambda: RecordWithFile)


class Record(RecordBase):
    """Object record API."""

    # Configuration
    model_cls = models.RecordMetadata

    # System fields
    schema = ConstantField(
        '$schema', 'https://coons.io/schemas/objects/object-v1.0.0.json')

    index = IndexField('objects-object-v1.0.0', search_alias='objects')

    pid = PIDField('id', provider=RecordIdProviderV2)

    dumper = ElasticsearchDumper(extensions=[ElasticsearchDumperObjectsExt()])


class RecordWithFile(Record):
    """Object record with file API."""

    files = FilesField(store=False, file_cls=RecordFile)
    bucket_id = ModelField()
    bucket = ModelField(dump=False)
