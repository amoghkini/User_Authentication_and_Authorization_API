import jwt
from datetime import datetime, timedelta
from flask import jsonify, request, g, make_response
from flask.views import MethodView
from sqlalchemy import text

from user.user_methods import UserMethods
from user.user_validations import LoginUser

class LoginAPI(MethodView):

    def post(self):
        # Parse the JSON request data
        data = request.get_json()
        status_code = None

        try:
            errors = LoginUser().validate(data)
            if errors:
                status_code = 422
                raise ValueError(errors)


            email = data.get('email')
            password = data.get('password')

            user = {"email" : email,
                    "password" : password}

            user = UserMethods.login_user(user)
            if user:
                # Add user login validations
                user_data = {
                    "id": user[0],
                    "email_id": user[1],
                    "first_name": user[2],
                    "role_id": user[4]}
                auth_token = UserMethods.generate_auth_token(user_data)
            else:
                status_code = 401
                raise ValueError("The entered login id or password is incorret")

            # Return a success message
            return make_response(jsonify({'status': 'success',
                                          'message': 'User logged in successfully',
                                          # Frontend needs to store this token in their session and send it on each new request.
                                          "token": auth_token if auth_token is not None else "",
                                          'data': []}), 200)
        except Exception as e:
            return make_response(jsonify({'status': 'error',
                                          'message': str(e),
                                          'data': None}), 401 if status_code == None else status_code)