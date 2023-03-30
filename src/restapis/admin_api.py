from flask import jsonify, make_response
from flask.views import MethodView

from user.authorization import Authorization as auth


class AdminAPI(MethodView):
    @auth.auth_required()
    def get(self):
        return make_response(jsonify({'status': 'success',
                                      'message': 'This is admin page',
                                      'data': []}), 200)
