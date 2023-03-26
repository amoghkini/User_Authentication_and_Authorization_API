from flask import jsonify, request, g, make_response, session
from flask.views import MethodView
from sqlalchemy import text

from psycopg2.errorcodes import UNIQUE_VIOLATION
from psycopg2 import errors


class LoginAPI(MethodView):
    def get(self):
        return "get method"
    
    def post(self):
        # Parse the JSON request data
        http_status_code = None
        data = request.get_json()
        try:
            email = data.get('email')
            password = data.get('password')  

            # Insert the new user into the database
            try:
                query = text('SELECT * FROM backtest.users WHERE email_id = :email_id AND password = :password')
                result = g.session.execute(query, {'email_id': email, 'password': password})

                # Retrieve the first row returned by the query
                user = result.fetchone()
                print(user)
                
                if user:
                    # Add user login validations 
                    session['user'] = user[1]
                    print(user[1])
                else:
                    http_status_code = 204
                    raise ValueError("The entered login id or password is incorret")
                
            except Exception as e:
                raise ValueError("Not able to fetch the user details... Please retry after sometime.")

            # Return a success message
            return make_response(jsonify({'status': 'success',
                                          'message': 'User logged in successfully',
                                          'data': []}), 200)
        except Exception as e:
            print(e)
            return make_response(jsonify({'status': 'error',
                                          'message': str(e),
                                          'data': None}), 200 if http_status_code == None else http_status_code)

# Curl requests
