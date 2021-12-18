# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Johnny Mariéthoz.
#
# Coons is free software; you can redistribute it and/or modify it under the
# terms of the MIT License; see LICENSE file for more details.

"""Objects permission policy."""

from elasticsearch_dsl.query import Q
from flask_login import current_user
from invenio_access.permissions import any_user, authenticated_user, \
    superuser_access, system_process
from invenio_records_permissions import RecordPermissionPolicy
from invenio_records_permissions.generators import AuthenticatedUser


class Read(AuthenticatedUser):
    """Read projects permissions."""

    def query_filter(self, identity=None, **kwargs):
        """Search filters."""
        if superuser_access in identity.provides:
            return Q('match_all')
        for need in identity.provides:
            if need.method == 'id':
                return Q('term', owners=need.value)
        return []


class PermissionPolicy(RecordPermissionPolicy):
    """Objects permission policy. All actions allowed."""

    # TODO: Use existing roles
    can_search = [Read()]
    can_create = [AuthenticatedUser()]
    can_read = [Read()]
    can_update = [AuthenticatedUser()]
    can_delete = [AuthenticatedUser()]
    can_create_files = [AuthenticatedUser()]
    can_read_files = [AuthenticatedUser()]
    can_update_files = [AuthenticatedUser()]
    can_delete_files = [AuthenticatedUser()]
