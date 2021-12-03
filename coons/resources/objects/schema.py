# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Johnny Mariéthoz.
#
# Coons is free software; you can redistribute it and/or modify it under the
# terms of the MIT License; see LICENSE file for more details.


"""Objects schema."""

from invenio_records_resources.resources import search_link_params, \
    search_link_when
from marshmallow import INCLUDE, Schema, ValidationError, fields, pre_load, \
    validate
from marshmallow_utils.fields import Link, Links
from uritemplate import URITemplate


class RDFObjectsSchema(Schema):
    """Basic metadata schema class."""

    class Meta:
        """Meta class to accept unknown fields."""

        unknown = INCLUDE

    _ref = fields.Str(required=True, attribute="$ref", data_key="$ref")
    predicate = fields.Str(required=True, validate=validate.Length(min=3))
    name = fields.Str(dump_only=True, validate=validate.Length(min=3))
    type = fields.Str(dump_only=True, validate=validate.Length(min=3))

    @pre_load
    def clean(self, data, **kwargs):
        """Removes dump_only fields."""
        data.pop('name', None)
        data.pop('type', None)
        return data


class MetadataSchema(Schema):
    """Basic metadata schema class."""

    class Meta:
        """Meta class to accept unknown fields."""

        unknown = INCLUDE

    name = fields.Str(required=True, validate=validate.Length(min=3))
    type = fields.Str(required=True, validate=validate.Length(min=3))
    content = fields.Str(validate=validate.Length(min=3))
    files = fields.Dict()
    objects = fields.List(fields.Nested(RDFObjectsSchema))


class BaseRecordSchema(Schema):
    """Schema for records v1 in JSON."""

    id = fields.Str()
    created = fields.Str(dump_only=True)
    updated = fields.Str(dump_only=True)
    links = Links(dump_only=True)
    revision_id = fields.Integer(dump_only=True)

    @pre_load
    def clean(self, data, **kwargs):
        """Removes dump_only fields."""
        data.pop('created', None)
        data.pop('updated', None)
        data.pop('links', None)
        data.pop('revision_id', None)
        return data


class RecordSchema(BaseRecordSchema):
    """Schema for records v1 in JSON."""

    metadata = fields.Nested(MetadataSchema)


class FilesLinksSchema(Schema):
    """Schema for a record's links."""

    # NOTE: /api prefix is needed here because above are mounted on /api
    self_ = Link(
        template=URITemplate("/api/objects/{pid_value}/files"),
        permission="read",
        params=lambda record: {
            'pid_value': record.pid.pid_value,
        },
        data_key="self"  # To avoid using self since is python reserved key
    )


class FileLinksSchema(Schema):
    """Schema for a record's links."""

    self_ = Link(
        template=URITemplate("/api/objects/{pid_value}/files/{key}"),
        permission="read",
        params=lambda record_file: {
            'pid_value': record_file.record.pid.pid_value,
            'key': record_file.key,
        },
        data_key="self"  # To avoid using self since is python reserved key
    )

    content = Link(
        template=URITemplate("/api/objects/{pid_value}/files/{key}/content"),
        permission="read",
        params=lambda record_file: {
            'pid_value': record_file.record.pid.pid_value,
            'key': record_file.key,
        },
    )

    commit = Link(
        template=URITemplate("/api/objects/{pid_value}/files/{key}/commit"),
        permission="read",
        params=lambda record_file: {
            'pid_value': record_file.record.pid.pid_value,
            'key': record_file.key,
        },
    )


class RecordLinksSchema(Schema):
    """Schema for a record's links."""

    # NOTE:
    #   - /api prefix is needed here because above are mounted on /api
    self_ = Link(
        template=URITemplate("/api/objects/{pid_value}"),
        permission="read",
        params=lambda record: {'pid_value': record.pid.pid_value},
        data_key="self"  # To avoid using self since is python reserved key
    )
    files = Link(
        template=URITemplate("/api/objects/{pid_value}/files"),
        permission="read",
        params=lambda record: {'pid_value': record.pid.pid_value},
    )


class SearchLinksSchema(Schema):
    """Schema for a search result's links."""

    # NOTE:
    #   - /api prefix is needed here because api routes are mounted on /api
    self = Link(
        template=URITemplate("/api/objects{?params*}"),
        permission="search",
        params=search_link_params(0),
    )
    prev = Link(
        template=URITemplate("/api/objects{?params*}"),
        permission="search",
        params=search_link_params(-1),
        when=search_link_when(-1)
    )
    next = Link(
        template=URITemplate("/api/objects{?params*}"),
        permission="search",
        params=search_link_params(+1),
        when=search_link_when(+1)
    )
