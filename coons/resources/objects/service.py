# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Johnny Mariéthoz.
#
# Coons is free software; you can redistribute it and/or modify it under the
# terms of the MIT License; see LICENSE file for more details.

"""Objects service."""

from invenio_records_resources.services import FileLink
from invenio_records_resources.services import FileService as BaseFileService
from invenio_records_resources.services import FileServiceConfig
from invenio_records_resources.services import \
    FileServiceConfig as BaseFileServiceConfig
from invenio_records_resources.services import RecordLink, RecordService, \
    RecordServiceConfig
from invenio_records_resources.services import \
    SearchOptions as BaseSearchOptions
from invenio_records_resources.services import pagination_links
from invenio_records_resources.services.records.facets import TermsFacet
from invenio_records_resources.services.records.params import FacetsParam, \
    PaginationParam, QueryStrParam, SortParam

from coons.resources.objects.results import HilightRecordList

from .api import RecordWithFile
from .identities import system_identity
from .params.highlight import HighlightParams
from .permissions import PermissionPolicy
from .results import HilightRecordList
from .schema import RecordSchema


class PreFacetsParam(FacetsParam):
    """."""

    def filter(self, search):
        """Apply a pre filter on the search."""
        if not self._filters:
            return search

        filters = list(self._filters.values())

        post_filter = filters[0]
        for f in filters[1:]:
            post_filter |= f

        return search.filter(post_filter)


class SearchOptions(BaseSearchOptions):
    """Search options."""

    facets = {
        'type': TermsFacet(field='metadata.type'),
        'predicate': TermsFacet(field='metadata.objects.predicate'),
        'object_type': TermsFacet(field='metadata.objects.type')
    }

    pagination_options = {
        "default_results_per_page": 10,
        "default_max_results": 10000
    }

    params_interpreters_cls = [
        QueryStrParam,
        PaginationParam,
        SortParam,
        PreFacetsParam,
        HighlightParams
    ]


class ServiceConfig(RecordServiceConfig):
    """Object service configuration.

    Needs both configs, with File overwritting the record ones.
    """

    permission_policy_cls = PermissionPolicy

    record_cls = RecordWithFile

    result_list_cls = HilightRecordList

    schema = RecordSchema

    # Search configuration
    search = SearchOptions

    links_item = {
        "self": RecordLink("{+api}/objects/{id}"),
    }

    links_search = pagination_links("{+api}/objects{?args*}")


class Service(RecordService):
    """Object service."""

    def update(self, id_, identity, data, links_config=None,
               revision_id=None):
        """Replace a record."""
        to_return = super().update(id_, identity, data, links_config)
        self.reindex_subjects(id_)
        return to_return

    def reindex_subjects(self, id_):
        """Reindex parents subjects given the id_."""
        search = self.search_request(
            system_identity, {}, self.record_cls, self.config.search)
        subjects_ids = [s.meta.id for s in search.filter(
            'term',
            **{'metadata.objects.$ref': 'https://coons.io/api/objects/' + id_}
        ).source(['id']).scan()]
        self.indexer.bulk_index(subjects_ids)
        self.indexer.process_bulk_queue()


class FileServiceConfig(BaseFileServiceConfig):
    """Object service configuration."""

    permission_policy_cls = PermissionPolicy
    record_cls = RecordWithFile
    file_links_list = {
        "self": RecordLink("{+api}/objects/{id}/files"),
    }

    file_links_item = {
        "self": FileLink("{+api}/objects/{id}/files/{key}"),
        "content": FileLink("{+api}/objects/{id}/files/{key}/content"),
        "commit": FileLink("{+api}/objects/{id}/files/{key}/commit"),
    }


class FileService(BaseFileService):
    """Object service."""

    default_config = FileServiceConfig
