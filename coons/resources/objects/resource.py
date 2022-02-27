# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Johnny Mariéthoz.
#
# Coons is free software; you can redistribute it and/or modify it under the
# terms of the MIT License; see LICENSE file for more details.

"""Objects resource."""

from invenio_records_resources.resources import FileResource, \
    FileResourceConfig, RecordResource, RecordResourceConfig


class CustomRecordResourceConfig(RecordResourceConfig):
    """Custom record resource configuration."""

    url_prefix = "/objects"
    blueprint_name = "objects"


class CustomRecordResource(RecordResource):
    """Custom record resource"."""


class CustomFileResourceConfig(FileResourceConfig):
    """Custom file resource configuration."""

    url_prefix = "/objects/<pid_value>"
    blueprint_name = "objects_files"


class CustomFileResource(FileResource):
    """Custom file resource."""
