# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Johnny Mariéthoz.
#
# Coons is free software; you can redistribute it and/or modify it under the
# terms of the MIT License; see LICENSE file for more details.

"""Identities."""

from flask_principal import Identity, Need, UserNeed

# identity for cli or system tasks
system_identity = Identity(1)
system_identity.provides.add(UserNeed(1))
system_identity.provides.add(Need(method="system_role", value="any_user"))
