# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Johnny Mariéthoz.
#
# Coons is free software; you can redistribute it and/or modify it under the
# terms of the MIT License; see LICENSE file for more details.

"""Default configuration for Coons.

You overwrite and set instance-specific configuration by either:

- Configuration file: ``<virtualenv prefix>/var/instance/invenio.cfg``
- Environment variables: ``APP_<variable name>``
"""

from datetime import timedelta

from invenio_app.config import APP_DEFAULT_SECURE_HEADERS
from invenio_oauthclient.contrib import github
from invenio_previewer.config import PREVIEWER_PREFERENCE as BASE_PREFERENCE


def _(x):
    """Identity function used to trigger string extraction."""
    return x


# Rate limiting
# =============
#: Storage for ratelimiter.
RATELIMIT_STORAGE_URL = 'redis://localhost:6379/3'

# I18N
# ====
#: Default language
BABEL_DEFAULT_LANGUAGE = 'en'
#: Default time zone
BABEL_DEFAULT_TIMEZONE = 'Europe/Zurich'
#: Other supported languages (do not include the default language in list).
I18N_LANGUAGES = [
    # ('fr', _('French'))
]

# Base templates
# # ==============
# #: Global base template.
# BASE_TEMPLATE = 'invenio_theme/page.html'
# #: Cover page base template (used for e.g. login/sign-up).
# COVER_TEMPLATE = 'invenio_theme/page_cover.html'
# #: Footer base template.
# FOOTER_TEMPLATE = 'invenio_theme/footer.html'
# #: Header base template.
# HEADER_TEMPLATE = 'invenio_theme/header.html'
# #: Settings base template.
# SETTINGS_TEMPLATE = 'invenio_theme/page_settings.html'

# # Theme configuration
# # ===================
# #: The Invenio theme.
APP_THEME = ['bootstrap3']
# #: Site name.
THEME_SITENAME = _('🦝 Coons')
THEME_LOGO = 'images/logo.svg'
# #: Use default frontpage.
THEME_FRONTPAGE = True
# #: Frontpage title.
THEME_FRONTPAGE_TITLE = _('🦝 Coons')
# #: Frontpage template.
THEME_FRONTPAGE_TEMPLATE = 'coons/frontpage.html'

THEME_FOOTER_TEMPLATE = 'coons/footer.html'

USERPROFILES_BASE_TEMPLATE = 'invenio_theme/page.html'
USERPROFILES_SETTINGS_TEMPLATE = 'invenio_theme/page_settings.html'


OAUTHCLIENT_REMOTE_APPS = dict(
    github=github.REMOTE_APP
)

# UI
# ==
#: Configure the search engine endpoint
# SEARCH_UI_SEARCH_API = '/api/objects'

#: Configure the results template
# SEARCH_UI_JSTEMPLATE_RESULTS = 'templates/coons/results.html'

# Email configuration
# ===================
#: Email address for support.
SUPPORT_EMAIL = "chezjohnny@gmail.com"
#: Disable email sending by default.
MAIL_SUPPRESS_SEND = True

# Assets
# ======
#: Static files collection method (defaults to copying files).
# COLLECT_STORAGE = 'flask_collect.storage.file'
COLLECT_STORAGE = 'flask_collect.storage.link'

# Accounts
# ========
#: Email address used as sender of account registration emails.
SECURITY_EMAIL_SENDER = SUPPORT_EMAIL
#: Email subject for account registration emails.
SECURITY_EMAIL_SUBJECT_REGISTER = _(
    "Welcome to Coons!")
#: Redis session storage URL.
ACCOUNTS_SESSION_REDIS_URL = 'redis://localhost:6379/1'
#: Enable session/user id request tracing. This feature will add X-Session-ID
#: and X-User-ID headers to HTTP response. You MUST ensure that NGINX (or other
#: proxies) removes these headers again before sending the response to the
#: client. Set to False, in case of doubt.
ACCOUNTS_USERINFO_HEADERS = True

# Celery configuration
# ====================

# BROKER_URL = 'amqp://guest:guest@localhost:5672/'
# #: URL of message broker for Celery (default is RabbitMQ).
# CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672/'
# #: URL of backend for result storage (default is Redis).
# CELERY_RESULT_BACKEND = 'redis://localhost:6379/2'
# #: Scheduled tasks configuration (aka cronjobs).
# CELERY_BEAT_SCHEDULE = {
#     'indexer': {
#         'task': 'invenio_indexer.tasks.process_bulk_queue',
#         'schedule': timedelta(minutes=5),
#     },
#     'accounts': {
#         'task': 'invenio_accounts.tasks.clean_session_table',
#         'schedule': timedelta(minutes=60),
#     },
# }

# Database
# ========
#: Database URI including user and password
SQLALCHEMY_DATABASE_URI = \
    'postgresql+psycopg2://coons:coons@localhost/coons'

# JSONSchemas
# ===========
#: Hostname used in URLs for local JSONSchemas.
JSONSCHEMAS_HOST = 'coons.io'

# Flask configuration
# ===================
# See details on
# http://flask.pocoo.org/docs/0.12/config/#builtin-configuration-values

#: Secret key - each installation (dev, production, ...) needs a separate key.
#: It should be changed before deploying.
SECRET_KEY = 'CHANGE_ME'
#: Max upload size for form data via application/mulitpart-formdata.
MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100 MiB
#: Sets cookie with the secure flag by default
SESSION_COOKIE_SECURE = True
#: Since HAProxy and Nginx route all requests no matter the host header
#: provided, the allowed hosts variable is set to localhost. In production it
#: should be set to the correct host and it is strongly recommended to only
#: route correct hosts to the application.
APP_ALLOWED_HOSTS = ['coons.io', 'localhost', '127.0.0.1']

# OAI-PMH
# =======
# OAISERVER_ID_PREFIX = 'oai:coons.io:'

# Previewers
# ==========
#: Include IIIF preview for images.
# PREVIEWER_PREFERENCE = ['iiif_image'] + BASE_PREFERENCE

# Debug
# =====
# Flask-DebugToolbar is by default enabled when the application is running in
# debug mode. More configuration options are available at
# https://flask-debugtoolbar.readthedocs.io/en/latest/#configuration

#: Switches off incept of redirects by Flask-DebugToolbar.
DEBUG_TB_INTERCEPT_REDIRECTS = False

# Configures Content Security Policy for PDF Previewer
# Remove it if you are not using PDF Previewer
APP_DEFAULT_SECURE_HEADERS['content_security_policy'] = {
    'default-src': ["'self'", "'unsafe-inline'"],
    'object-src': ["'none'"],
    'style-src': [
        "'self'", "'unsafe-inline'", "https://fonts.googleapis.com",
        "https://maxcdn.bootstrapcdn.com"
    ],
    'font-src': [
        "'self'", "data:", "https://fonts.gstatic.com",
        "https://maxcdn.bootstrapcdn.com"
    ]
}

# #: for legacy compatibility
# RECORDS_REST_ENDPOINTS = {}

# #: record detailed views
# RECORDS_UI_ENDPOINTS = {
#     "docid": {
#         "pid_type": "recid",
#         "route": "/objects/<pid_value>",
#         "template": "bootstrap3/coons/detail.html",
#         "record_class": "coons.resources.objects.api.RecordWithFile"
#     }
# }

# TODO: remove this in production
RATELIMIT_ENABLED = False

COONS_SUPPORTED_MIME_TYPES = "*"

ACCOUNTS_REST_AUTH_VIEWS = {
    "login": "invenio_accounts.views.rest:LoginView",
    "logout": "invenio_accounts.views.rest:LogoutView",
    "user_info": "coons.rest:UserInfoView",
    "register": "invenio_accounts.views.rest:RegisterView",
    "forgot_password": "invenio_accounts.views.rest:ForgotPasswordView",
    "reset_password": "invenio_accounts.views.rest:ResetPasswordView",
    "change_password": "invenio_accounts.views.rest:ChangePasswordView",
    "send_confirmation":
        "invenio_accounts.views.rest:SendConfirmationEmailView",
    "confirm_email": "invenio_accounts.views.rest:ConfirmEmailView",
    "sessions_list": "invenio_accounts.views.rest:SessionsListView",
    "sessions_item": "invenio_accounts.views.rest:SessionsItemView"
}
