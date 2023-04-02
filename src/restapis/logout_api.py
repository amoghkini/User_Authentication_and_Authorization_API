from flask import jsonify, make_response
from flask.views import MethodView

from user.authorization import Authorization as auth
from user.user_methods import UserMethods

class LogoutAPI(MethodView):
    
    @auth.auth_required()
    def get(self):
        try:

            UserMethods.logout_user()
            
            return make_response(jsonify({'status': 'success',
                                      'message': 'User logged out successfully',
                                      'data': []}), 200)            
        except Exception as e:
            return make_response(jsonify({'status': 'error',
                                          'message': str(e),
                                          'data': None}), 422)
