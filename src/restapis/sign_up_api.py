from flask import jsonify, request, g, make_response, url_for
from flask.views import MethodView
from psycopg2.errorcodes import UNIQUE_VIOLATION
from psycopg2 import errors
from sqlalchemy import text

from user.user import User
from user.user_methods import UserMethods
from user.user_validations import SignUpUser

class SignUpAPI(MethodView):      
        
    def post(self):
        # Parse the JSON request data
        
        data = request.get_json()
        
        errors = SignUpUser().validate(data)
        
        if errors:
            return errors, 422
        
        try:
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            email = data.get('email')
            
            # Insert the new user into the database
            try:
                user = User(email, first_name, last_name)
                user.password = data.get('password')
                user.confirm_password = data.get('confirm_password')
                user.mobile_no = data.get('mobile_no')
                user.date_of_birth = data.get('date_of_birth')
                
                query = text('INSERT INTO backtest.users (first_name, last_name, email_id, password, mobile_no) VALUES (:first_name, :last_name, :email_id, :password, :mobile_no)')
                g.session.execute(query, {'first_name': first_name, 'last_name': last_name,
                                  'email_id': email, 'password': user.password, 'mobile_no': user.mobile_no})
                g.session.commit()

                verify_token = UserMethods.generate_token(email)
                link = f'''Click here to verify the account: {url_for('verify_email_api', token=verify_token, _external=True)}'''
                print("Link", link)
            # UniqueViolation exception not working as of now. Will check this later.
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