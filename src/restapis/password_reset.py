from flask import jsonify, g, make_response, request
from flask.views import MethodView
from sqlalchemy import text

from user.user_methods import UserMethods


class PasswordResetAPI(MethodView):
    def get(self, token):

        email = UserMethods.decode_token(token)

        query = text(
            'SELECT user_id, email_id, first_name, account_creation_date, role_id FROM backtest.users WHERE email_id = :email_id')
        result = g.session.execute(query, {'email_id': email})

        # Retrieve the first row returned by the query
        user = result.fetchone()

        if user:
            return make_response(jsonify({'status': 'success',
                                          'message': 'Password can be changed!!!',
                                          'data': []}), 200)
        else:
            return make_response(jsonify({'status': 'error',
                                          'message': 'The password reset link is either expired or invalid. \
                                                      Please try to reset the account again.',
                                          'data': None}), 404)

    def post(self,token):
        
        email = UserMethods.decode_token(token)
        print(email)
        
        if not email:
            return make_response(jsonify({'status': 'error',
                                          'message': 'The password reset link is either expired or invalid.',
                                          'data': None}), 404)
        query = text(
            'SELECT user_id, email_id, first_name, account_creation_date, role_id FROM backtest.users WHERE email_id = :email_id')
        result = g.session.execute(query, {'email_id': email})

        # Retrieve the first row returned by the query
        user = result.fetchone()

        data = request.get_json()
        print(data)

        if user:
            # verify the password
            # Save the updated password in the database.
            return make_response(jsonify({'status': 'success',
                                          'message': 'Password changed successfully',
                                          'data': []}), 200)
        else:
            return make_response(jsonify({'status': 'error',
                                          'message': 'The user is not registered in the system.',
                                          'data': None}), 404)