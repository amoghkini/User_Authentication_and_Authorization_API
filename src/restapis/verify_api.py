from flask import jsonify, g, make_response
from flask.views import MethodView
from sqlalchemy import text
from sqlalchemy.exc import InvalidRequestError

from user.user_methods import UserMethods
from user.user_status import UserStatus

class VerifyUserAPI(MethodView):
    def get(self,token):
        
        try:
            email = UserMethods.decode_token(token)
            
            if not email:
                raise ValueError('The account verification link is either expired or invalid. Please try to login to verify the account.')
                
            query = text(
                'SELECT user_id, email_id, first_name, account_creation_date, role_id FROM backtest.users WHERE email_id = :email_id')
            result = g.session.execute(query, {'email_id': email})

            # Retrieve the first row returned by the query
            user = result.fetchone()
            if user:
                
                query = text('UPDATE backtest.users SET account_status= :account_status WHERE email_id= :email_id')
                g.session.execute(query, {'account_status': UserStatus.ACTIVATED, 'email_id': email})
                g.session.commit()
                
                return make_response(jsonify({'status': 'success',
                            'message': 'Account verified!!! Redirecting user to login page!',
                            'data': []}), 200)
            else:
                raise ValueError('The account verification link is either expired or invalid. Please try to login and verify the account.')
        
        # Not able to handle below exception. Need to check in later stages of development.
        except InvalidRequestError as e:
            raise ValueError("Something went wrong... Please retry after sometime!!!")
        
        except Exception as e:
            return make_response(jsonify({'status': 'error',
                                          'message': str(e),
                                          'data': None}), 404)
