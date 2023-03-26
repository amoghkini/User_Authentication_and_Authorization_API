from flask import session, jsonify, make_response
from flask.views import MethodView

class LogoutAPI(MethodView):
    
    def get(self):
        try:
            session.pop('user',None)
        
            return make_response(jsonify({'status': 'success',
                                      'message': 'User logged out successfully',
                                      'data': []}), 200)
        except Exception as e:
            return make_response(jsonify({'status': 'error',
                                          'message': str(e),
                                          'data': None}), 200)
