# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Johnny Mariéthoz.
#
# Coons is free software; you can redistribute it and/or modify it under the
# terms of the MIT License; see LICENSE file for more details.

"""Objects es params."""
from invenio_records_resources.services.records.results import RecordList


class HilightRecordList(RecordList):
    """."""

    @property
    def hits(self):
        """Iterator over the hits."""
        for hit in self._results:
            # Load dump
            record = self._service.record_cls.loads(hit.to_dict())

            # Project the record
            projection = self._schema.dump(
                record,
                context=dict(
                    identity=self._identity,
                    record=record,
                )
            )
            if self._links_item_tpl:
                projection['links'] = self._links_item_tpl.expand(record)
            if hasattr(hit.meta, 'highlight'):
                projection['highlight'] = hit.meta.highlight.to_dict()
            yield projection
