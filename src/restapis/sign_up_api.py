from flask import jsonify, request, g, make_response, url_for
from flask.views import MethodView
from psycopg2.errorcodes import UNIQUE_VIOLATION
from psycopg2 import errors
from sqlalchemy import text

from messages.email import Email
from user.user import User
from user.user_methods import UserMethods
from user.user_validations import SignUpUser

class SignUpAPI(MethodView):      
        
    def post(self):
        # Parse the JSON request data
        data = request.get_json()
        status_code = None
            
        try:
            errors = SignUpUser().validate(data)
            if errors:
                status_code = 422
                raise ValueError(errors)
            
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            email = data.get('email')
            
    
            user = User(first_name, last_name)
            user.email = data.get('email')
            user.password = data.get('password')
            user.user_name = UserMethods.generate_username(first_name, last_name)
            user.mobile_no = data.get('mobile_no')
            user.date_of_birth = data.get('date_of_birth')
            
            UserMethods.sign_up_user(user)
                                
            verify_token = UserMethods.generate_token(email) # Generate account activation token.
            link = f'''Click here to verify the account: {url_for('verify_email_api', token=verify_token, _external=True)}'''
            Email.send_user_verification_email(link) # Send acccount activation link to given email address.
    
            # Return a success message
            return make_response(jsonify({'status':'success',
                            'message': 'User created successfully',
                            'data': []}), 201)
        except Exception as e:
            return make_response(jsonify({'status': 'error',
                            'message': str(e),
                            'data':None}), 200 if status_code == None else status_code)


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