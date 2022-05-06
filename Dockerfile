# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Johnny Mariéthoz.
#
# Coons is free software; you can redistribute it and/or modify it under the
# terms of the MIT License; see LICENSE file for more details.
#
# Dockerfile that builds a fully functional image of your app.
#
# Note: It is important to keep the commands in this file in sync with your
# boostrap script located in ./scripts/bootstrap.
#
# In order to increase the build speed, we are extending this image from a base
# image (built with Dockerfile.base) which only includes your Python
# dependencies.

ARG VERSION=latest
FROM coons-base:${VERSION}

USER 0

WORKDIR ${WORKING_DIR}/src
COPY ./docker/uwsgi/ ${INVENIO_INSTANCE_PATH}
COPY --chown=invenio:invenio  . ${WORKING_DIR}/src

# invenio user
USER 1000

RUN pipenv install --skip-lock . && \
    npm install --loglevel=error --no-save --only=prod --no-fund --no-audit  ./ui/coons-ui-core-1.1.0.tgz  --prefix "/invenio/var/instance/static" && \
    pipenv run invenio collect -v  && \
    pipenv run invenio webpack create && \
    pipenv run invenio webpack install && \
    pipenv run invenio webpack build && \
    pipenv run invenio webpack clean && \
    npm cache clean --force && \
    pipenv run pip cache purge

ENTRYPOINT [ "bash", "-c"]
