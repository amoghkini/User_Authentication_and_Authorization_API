from flask import jsonify, request, g, make_response
from flask.views import MethodView
from sqlalchemy import text

from psycopg2.errorcodes import UNIQUE_VIOLATION
from psycopg2 import errors


engine = None

class SignUpAPI(MethodView):
    def get(self):
        # Retrieve all users from the database
        query = "SELECT * FROM users"
        return query
        '''
        with engine.connect() as connection:
            result = connection.execute(query)
            users = result.fetchall()

        # Convert the users to a JSON response
        users_dict = [{'id': u[0], 'username': u[1], 'email': u[2]}
                      for u in users]
        return jsonify(users_dict)
        '''
        
    def post(self):
        # Parse the JSON request data
        data = request.get_json()
        try:
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            email = data.get('email')
            password = data.get('password')
            confirm_password = data.get('confirm_password')
            mobile_no = data.get('mobile_no')
            date_of_birth = data.get('date_of_birth')

            if len(email) < 10:
                raise ValueError("Invalid email address")
            
            # Insert the new user into the database
            try:
                query = text('INSERT INTO backtest.users (first_name, last_name, email_id, password, mobile_no) VALUES (:first_name, :last_name, :email_id, :password, :mobile_no)')
                g.session.execute(query, {'first_name': first_name, 'last_name': last_name, 'email_id': email, 'password': password, 'mobile_no': mobile_no})
                g.session.commit()
            
            except errors.UniqueViolation:
                print("UNIQUE VIOLATION")
                raise ValueError("The email address or mobile number is already exist.")
            
            except errors.lookup(UNIQUE_VIOLATION):
                print("Duplicate entry")
                #g.session.rollback()
                raise ValueError("The email address or mobile number is already exist.")
            
            except Exception as e:
                '''
                from psycopg2._psycopg import sqlstate_errors
                print(sqlstate_errors.get('23505'))
                '''
                
                g.session.rollback()
                print("EXCEPTION==",e)
                raise ValueError("Error while writing the data... Please retry after sometime.")

            # Return a success message
            return make_response(jsonify({'status':'success',
                            'message': 'User created successfully',
        
                            'data': []}), 201)
        except Exception as e:
            print(e)
            return make_response(jsonify({'status': 'error',
                            'message': str(e),
                            'data':None}), 200)


#### Curl requests
# Get
'''
curl --location '127.0.0.1:5000/signup' \
--header 'Cookie: session=eyJfcGVybWFuZW50Ijp0cnVlfQ.ZB4G7A.y2lhf_0MRCrashgOEAt-KjdllNY'
'''

# Post
'''
curl --location '127.0.0.1:5000/signup' \
--header 'Content-Type: application/json' \
--header 'Cookie: session=eyJfcGVybWFuZW50Ijp0cnVlfQ.ZB4I3g.AZxmKk56T4A6p3pKqLPBeZrbQdg' \
--data-raw '{
    "first_name" : "test_first_name",
    "last_name" : "test_last_name",
    "email" : "test_email",
    "password" : "password@123",
    "confirm_password" : "password@123",
    "mobile_no" : "9876543210",
    "date_of_birth" : "1970-01-31"
}'
'''