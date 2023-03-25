from flask import jsonify
from flask.views import MethodView

class IndexAPI(MethodView):

    def get(self):
        return jsonify({'status': 'success',
                        'message': 'This is public page',
                        'data': []})
