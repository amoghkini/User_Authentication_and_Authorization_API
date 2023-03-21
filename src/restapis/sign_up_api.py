from flask import render_template
from flask.views import MethodView

class SignUpAPI(MethodView):
    
    def get(self):
        return 'signup api'

    def post():
        pass