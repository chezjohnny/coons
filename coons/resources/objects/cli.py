# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Johnny Mariéthoz.
#
# Coons is free software; you can redistribute it and/or modify it under the
# terms of the MIT License; see LICENSE file for more details.

"""Objects Command Line Interface."""

import click
from flask.cli import with_appcontext

from ... import current_coons


@click.group()
def objects():
    """Objects management commands."""


@objects.command('reindex')
@with_appcontext
def reindex():
    """Reindex all the objects."""
    s = current_coons.resources['obj'].service
    ids = [s.id for s in s.record_cls.model_cls.query.all()]
    s.indexer.bulk_index(ids)
    res = s.indexer.process_bulk_queue()
