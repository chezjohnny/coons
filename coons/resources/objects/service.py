# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Johnny Mariéthoz.
#
# Coons is free software; you can redistribute it and/or modify it under the
# terms of the MIT License; see LICENSE file for more details.

"""Objects service."""

from invenio_records_resources.services import RecordFileService, \
    RecordFileServiceConfig
from invenio_records_resources.services.records.search import terms_filter

from .api import Record, RecordWithFile
from .identities import system_identity
from .permissions import PermissionPolicy
from .schema import RecordSchema


class ServiceConfig(RecordFileServiceConfig):
    """Object service configuration.

    Needs both configs, with File overwritting the record ones.
    """

    permission_policy_cls = PermissionPolicy
    record_cls = RecordWithFile
    schema = RecordSchema
    search_facets_options = {
        'aggs': {
            'type': {
                'terms': {'field': 'metadata.type'}
            },
            'predicate': {
                'terms': {'field': 'metadata.objects.predicate'}
            },
            'object_type': {
                'terms': {'field': 'metadata.objects.type'}
            }
        },
        'post_filters': {
            'type': terms_filter('metadata.type'),
            'predicate': terms_filter('metadata.objects.predicate'),
            'object_type': terms_filter('metadata.objects.type')
        }
    }


class Service(RecordFileService):
    """Object service."""

    default_config = ServiceConfig

    def update(self, id_, identity, data, links_config=None,
               revision_id=None):
        """Replace a record."""
        to_return = super().update(id_, identity, data, links_config)
        self.reindex_subjects(id_)
        return to_return

    def reindex_subjects(self, id_):
        """Reindex parents subjects given the id_."""
        search = self.search_request(system_identity, {}, self.record_cls)
        subjects_ids = [s.meta.id for s in search.filter(
            'term',
            **{'metadata.objects.$ref': 'https://coons.io/api/objects/' + id_}
        ).source(['id']).scan()]
        self.indexer.bulk_index(subjects_ids)
        self.indexer.process_bulk_queue()


class FileServiceConfig(RecordFileServiceConfig):
    """Object service configuration."""

    permission_policy_cls = PermissionPolicy
    record_cls = RecordWithFile


class FileService(RecordFileService):
    """Object service."""

    default_config = FileServiceConfig
