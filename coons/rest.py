"""Updated version of invenio-accounts REST API."""

from flask import current_app, jsonify
from flask.views import MethodView
from flask_login import login_required
from flask_security import current_user
from invenio_accounts.views.rest import default_user_payload


class UserInfoView(MethodView):
    """View to fetch info from current user."""

    decorators = [login_required]

    def success_response(self, user):
        """Return a successful user info response."""
        data = default_user_payload(user)
        data['config'] = dict(
            supported_mime_types=current_app.config.get(
                'COONS_SUPPORTED_MIME_TYPES'))
        return jsonify(data)

    def get(self):
        """Return user info."""
        return self.success_response(current_user)
