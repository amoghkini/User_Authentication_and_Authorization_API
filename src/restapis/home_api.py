from flask import jsonify
from flask.views import MethodView

class HomeAPI(MethodView):
    
    def get(self):
        return jsonify({'status': 'success',
                        'message': 'This is private page',
                        'data': []})
    
    