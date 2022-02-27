# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Johnny Mariéthoz.
#
# Coons is free software; you can redistribute it and/or modify it under the
# terms of the MIT License; see LICENSE file for more details.

"""Coons Main Application."""

from coons.resources.objects.resource import CustomFileResourceConfig, \
    CustomRecordResourceConfig
from coons.resources.objects.service import FileServiceConfig, ServiceConfig

from .theme.filters import node_assets


class Coons(object):
    """coons extension."""

    def __init__(self, app=None):
        """Coons App module."""
        self.resources = {}
        if app:
            self.init_app(app)
            app.add_template_global(node_assets, name='node_assets')

    def init_app(self, app):
        """Flask application initialization."""
        self.init_config(app)
        self.create_resources(app)
        app.extensions['coons'] = self

    def init_config(self, app):
        """Initialize configuration."""
        for k in dir(app.config):
            if k.startswith('COONS_APP_'):
                app.config.setdefault(k, getattr(app.config, k))

    def create_resources(self, app):
        """."""
        # imports should be here to avoid test errors
        from .resources.objects.resource import CustomFileResource, \
            CustomRecordResource
        from .resources.objects.service import FileService, Service

        # /api/objects
        objects_service = Service(ServiceConfig())
        objects_resource = CustomRecordResource(
            service=objects_service,
            config=CustomRecordResourceConfig)
        self.resources['obj'] = objects_resource

        # /api/objects/<>/files
        objects_files_service = FileService(FileServiceConfig())
        objects_files_resource = CustomFileResource(
            service=objects_files_service,
            config=CustomFileResourceConfig())
        self.resources['obj_files'] = objects_files_resource


class CoonsAPI(Coons):
    """coons extension."""

    def __init__(self, app=None):
        """Coons App module."""
        super().__init__(app)
        self.register_blueprints(app)

    def register_blueprints(self, app):
        """Register the blueprints."""
        app.register_blueprint(
            self.resources['obj'].as_blueprint())

        app.register_blueprint(
            self.resources['obj_files'].as_blueprint())
