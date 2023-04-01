from flask import jsonify, g, make_response
from flask.views import MethodView
from sqlalchemy import text

from user.user_methods import UserMethods

class VerifyUserAPI(MethodView):
    def get(self,token):
        
        email = UserMethods.decode_token(token)
        
        if not email:
            return make_response(jsonify({'status': 'error',
                                          'message': 'The password reset link is either expired or invalid.',
                                          'data': None}), 404)
            
        query = text(
            'SELECT user_id, email_id, first_name, account_creation_date, role_id FROM backtest.users WHERE email_id = :email_id')
        result = g.session.execute(query, {'email_id': email})

        # Retrieve the first row returned by the query
        user = result.fetchone()

        if user:
            return make_response(jsonify({'status': 'success',
                        'message': 'Account verified!!! Redirecting user to login page!',
                        'data': []}), 200)
        else:
            return make_response(jsonify({'status': 'error',
                                          'message': 'The account verification link is either expired or invalid. Please try to login to verify the account.',
                                          'data': None}), 404)
