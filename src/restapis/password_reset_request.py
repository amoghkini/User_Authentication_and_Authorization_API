from flask import jsonify, request, g, make_response, url_for
from flask.views import MethodView
from sqlalchemy import text

from user.user_methods import UserMethods

class PasswordRestRequestAPI(MethodView):

    def post(self):
        print("Amogh is here")
        # Parse the JSON request data
        data = request.get_json()
        print(data)
        try:
            
            email = data.get('email')

            # Insert the new user into the database
            try:
                query = text('SELECT user_id, email_id, first_name, account_creation_date, role_id FROM backtest.users WHERE email_id = :email_id')
                result = g.session.execute(query, {'email_id': email})

                # Retrieve the first row returned by the query
                user = result.fetchone()
                print(user)

                if user:
                    # Generate the password reset link
                    verify_token = UserMethods.generate_token(email)
                    link = f'''Click here to reset the password: {url_for('password_reset_api', token=verify_token, _external=True)}'''
                    print("Link", link)

            except Exception as e:
                raise ValueError(
                    "Something went wrong... Please retry after sometime.")

            # Return a success message
            return make_response(jsonify({'status': 'success',
                                          'message': 'The password reset link has been sent successfully on registered email address',
                                          'data': []}), 200)
        except Exception as e:
            print(e)
            return make_response(jsonify({'status': 'error',
                                          'message': str(e),
                                          'data': None}), 401 )

# Curl requests
