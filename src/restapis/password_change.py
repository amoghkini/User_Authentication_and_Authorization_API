from flask import jsonify, g, make_response, request
from flask.views import MethodView
from sqlalchemy import text

from user.authorization import Authorization as auth
from user.user_methods import UserMethods


class PasswordChangeAPI(MethodView):
    
    @auth.auth_required()
    def post(self):

        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if not email:
            return make_response(jsonify({'status': 'error',
                                          'message': 'The email address provided is incorrect.',
                                          'data': None}), 404)
        query = text(
            'SELECT user_id, email_id, first_name, account_creation_date, role_id FROM backtest.users WHERE email_id = :email_id')
        result = g.session.execute(query, {'email_id': email})

        # Retrieve the first row returned by the query
        user = result.fetchone()


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
