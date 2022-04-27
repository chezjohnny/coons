# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Johnny Mariéthoz.
#
# Coons is free software; you can redistribute it and/or modify it under the
# terms of the MIT License; see LICENSE file for more details.

"""Objects es params."""

from invenio_records_resources.services.records.params import ParamInterpreter


class HighlightParams(ParamInterpreter):
    """Evaluate a highlight parameter."""

    def __init__(self, config):
        """Initialise the parameter interpreter."""
        self.config = config

    def apply(self, identity, search, params):
        """Apply the parameters."""
        # options
        search = search.highlight_options(
            pre_tags='<mark>', post_tags='</mark>', fragment_size='30')
        # set the field
        search = search.highlight('metadata.content')
        return search.highlight('metadata.content')
