from flask.views import MethodView


class IndexAPI(MethodView):

    def get(self):
        return "This is public page"
