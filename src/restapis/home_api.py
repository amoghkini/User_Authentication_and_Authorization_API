from flask import jsonify, make_response
from flask.views import MethodView

from user.authorization import Authorization as auth

class HomeAPI(MethodView):
    @auth.auth_required()
    def get(self):

        return make_response(jsonify({'status': 'success',
                                      'message': 'This is private page',
                                      'data': []}), 200)
