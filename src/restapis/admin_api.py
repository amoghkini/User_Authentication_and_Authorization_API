from flask import jsonify
from flask.views import MethodView

from user.authorization import Authorization as auth


class AdminAPI(MethodView):
    @auth.auth_required()
    def get(self):
        return jsonify({'status': 'success',
                        'message': 'This is admin page',
                        'data': []})
