from flask import jsonify, g, make_response, request
from flask.views import MethodView
from sqlalchemy import text

from user.authorization import Authorization as auth
from user.user_methods import UserMethods
from user.user_validations import ChangePassword

class PasswordChangeAPI(MethodView):
    
    @auth.auth_required()
    def post(self):
        # Parse the JSON request data
        data = request.get_json()
        status_code = None

        try:
            errors = ChangePassword().validate(data)
            if errors:
                status_code = 422
                raise ValueError(errors)


            user = {"email": data.get('email'),
                    "old_password": data.get('old_password'),
                    "new_password": data.get('new_password'),
                    "confirm_new_password": data.get('confirm_new_password')}

            UserMethods.change_password(user)
    
            # Return a success message
            return make_response(jsonify({'status': 'success',
                                          'message': 'Password changed successfully',
                                          'data': []}), 200)
        except Exception as e:
            return make_response(jsonify({'status': 'error',
                                          'message': str(e),
                                          'data': None}), 401 if status_code == None else status_code)