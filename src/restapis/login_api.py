import jwt
from datetime import datetime, timedelta
from flask import jsonify, request, g, make_response, session
from flask.views import MethodView
from sqlalchemy import text

from psycopg2.errorcodes import UNIQUE_VIOLATION
from psycopg2 import errors


class LoginAPI(MethodView):
    
    def post(self):
        # Parse the JSON request data
        http_status_code = None
        data = request.get_json()
        try:
            email = data.get('email')
            password = data.get('password')  

            # Insert the new user into the database
            try:
                query = text('SELECT user_id, email_id, first_name, account_creation_date, role_id FROM backtest.users WHERE email_id = :email_id AND password = :password')
                result = g.session.execute(query, {'email_id': email, 'password': password})

                # Retrieve the first row returned by the query
                user = result.fetchone()
                print(user)

                if user:
                    # Add user login validations 
                    session['user'] = user[1]
                    user_data = {
                        "id" : user[0],
                        "email_id" : user[1],
                        "first_name": user[2],
                        "account_creation_date": user[3],
                        "role_id": user[4]
                    }
                    exp_time = datetime.now() + timedelta(minutes=15)
                    exp_epoch_time = int(exp_time.timestamp())
                    data = {
                        "payload": user_data,
                        "exp": exp_epoch_time
                    }
                    auth_token = jwt.encode(data, "secret_key", algorithm="HS256")
                else:
                    http_status_code = 204
                    raise ValueError("The entered login id or password is incorret")
                
            except Exception as e:
                raise ValueError("Not able to fetch the user details... Please retry after sometime.")

            # Return a success message
            return make_response(jsonify({'status': 'success',
                                          'message': 'User logged in successfully',
                                          "token": auth_token if auth_token is not None else "",
                                          'data': []}), 200)
        except Exception as e:
            print(e)
            return make_response(jsonify({'status': 'error',
                                          'message': str(e),
                                          'data': None}), 401 if http_status_code == None else http_status_code)

# Curl requests

