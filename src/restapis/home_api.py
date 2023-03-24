from flask.views import MethodView

class HomeAPI(MethodView):
    
    def get(self):
        return "This is protected page"
    
    