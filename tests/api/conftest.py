# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Johnny Mariéthoz.
#
# Coons is free software; you can redistribute it and/or modify it under the
# terms of the MIT License; see LICENSE file for more details.

"""Pytest fixtures and plugins for the API application."""

import tempfile

import pytest
from invenio_app.factory import create_api
from invenio_files_rest.models import Location
from invenio_records_rest.utils import allow_all


@pytest.fixture(scope='module')
def app_config(app_config):
    """Get app config."""
    app_config['RECORDS_FILES_REST_ENDPOINTS'] = {
        'RECORDS_REST_ENDPOINTS': {
            'recid': '/files'
        }
    }
    app_config['FILES_REST_PERMISSION_FACTORY'] = allow_all
    app_config['CELERY_ALWAYS_EAGER'] = True
    return app_config


@pytest.fixture(scope='module')
def create_app():
    """Create test app."""
    return create_api
