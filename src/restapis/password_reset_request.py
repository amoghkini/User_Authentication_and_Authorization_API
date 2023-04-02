from flask import jsonify, request, g, make_response, url_for
from flask.views import MethodView
from sqlalchemy import text

from messages.email import Email
from user.user_methods import UserMethods

class PasswordRestRequestAPI(MethodView):
    
    def post(self):
        # Parse the JSON request data
        data = request.get_json()
        status_code = None

        try:
            email = data.get('email')
            
            user = UserMethods.get_user(email)
            if user:
                # Generate the password reset link
                verify_token = UserMethods.generate_token(email)
                link = f'''Click here to reset the password: {url_for('password_reset_api', token=verify_token, _external=True)}'''
                Email.send_password_activation_email(link)  # Send acccount activation link to given email address.

            # Return a success message
            return make_response(jsonify({'status': 'success',
                                          'message': 'The password reset link has been sent successfully on registered email address',
                                          'data': []}), 200)
        except Exception as e:
            return make_response(jsonify({'status': 'error',
                                          'message': str(e),
                                          'data': None}), 401 if status_code == None else status_code)
