#!/usr/bin/env bash
# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Johnny Mariéthoz.
#
# Coons is free software; you can redistribute it and/or modify it under the
# terms of the MIT License; see LICENSE file for more details.


# Quit on errors
set -o errexit

# Quit on unbound symbols
set -o nounset

# # Always bring down docker services
# function cleanup() {
#     eval "$(docker-services-cli down --env)"
# }
# trap cleanup EXIT

# Check vulnerabilities
# TODO: solve this
pipenv check -i 42852 -i 42050 -i 42194 -i 40459 -i 42498

pipenv run python -m check_manifest --ignore ".*-requirements.txt"
# eval "$(docker-services-cli up --db ${DB:-postgresql} --search ${SEARCH:-elasticsearch} --cache ${CACHE:-redis} --mq ${MQ:-rabbitmq} --env)"
pipenv run python -m pytest
tests_exit_code=$?
pipenv run python -m sphinx.cmd.build -qnNW -b doctest docs docs/_build/doctest

exit "$tests_exit_code"
