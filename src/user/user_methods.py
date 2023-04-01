import jwt
from datetime import datetime, timedelta
from flask import request, make_response, jsonify, g
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy import text

from user.auth_token_status import AuthTokenStatus
from utils.utils import Utils

class UserMethods:
    
    @staticmethod
    def add_new_user():
        return
    
    @staticmethod
    def logout_user():
        authorization = request.headers.get("authorization")
        if authorization:
            token = authorization.split(" ")[1]
        else:
            token = ''
            
        if token:
            # Add entry in blacklisted_tokens table and pass the success message on the screen.
            # Refer: https://github.com/realpython/flask-jwt-auth/blob/master/project/server/auth/views.py
            query = text('INSERT INTO backtest.blacklisted_tokens (token, blacklisted_on, blacklisting_reason) VALUES (:token, :blacklisted_on, :blacklisting_reason)')
            g.session.execute(query, {'token': token, 'blacklisted_on': Utils.getEpoch(), 'blacklisting_reason': AuthTokenStatus.LOG_OUT})
            g.session.commit()
            
        else:
            raise ValueError("Invalid Token")

    @staticmethod
    def generate_auth_token(user_data):
        try:
            exp_time = datetime.now() + timedelta(minutes=15)
            exp_epoch_time = int(exp_time.timestamp())
            data = {"payload": user_data,
                    "exp": exp_epoch_time
                        }
            return jwt.encode(data, "secret_key", algorithm="HS256")
        except Exception as e:
            raise ValueError()
    
    @staticmethod
    def decode_auth_token(auth_token: str):
        try:
            is_blacklisted_token = UserMethods.check_if_token_is_blacklisted(auth_token)
            if is_blacklisted_token:
                raise ValueError("Token is blacklisted. Please login again!!")
            else:
                tokendata = jwt.decode(auth_token, "secret_key", algorithms="HS256")
                return tokendata.get('payload').get('role_id')
            
        except jwt.ExpiredSignatureError:
            raise ValueError("Token Expired!!! Please login again")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token!! Please login again")
        
    @staticmethod
    def check_if_token_is_blacklisted(auth_token: str):
        query = text('SELECT * FROM backtest.blacklisted_tokens WHERE token = :token')
        result = g.session.execute(query, {'token': auth_token})
        response = result.fetchone()
        
        if response:
            return True
        else:
            return False
    
    @staticmethod
    def generate_token(user_id, secret_key='secret_key', epires_sec = 100):
        """
        Generates a time-limited token. It can be used for following instances.
        1. Verifying the email address of a user.
        2. To reset the password.

        Args:
            user_id (str): The unique email address of the user which needs to be verified.
            secret_key (str): A secret key used for generating the token. This should be kept secure.
            expires_sec (int, optional): The expiration time for the token, in seconds. Defaults to 1800 seconds (30 minutes).

        Returns:
            str: The generated verification token as a string.

        Raises:
            None.
        """
        
        s = Serializer(secret_key, epires_sec) # need to figure out how to pass secret key. It can be from config file or env.# need to figure out how to pass secret key. It can be from config file or env.
        return s.dumps({'user_id':user_id}).decode('utf-8') 
    
    @staticmethod
    def decode_token(token, secret_key='secret_key'):
        """
        Decodes a token to retrieve the user ID of the associated user.

        Args:
            token (str): The reset token to decode.
            secret_key (str): The secret key used for generating the token.

        Returns:
            Union[str, None]: If decoding the token is successful, the user ID associated with the token is returned as a string.
            If decoding the token fails, None is returned.

        Raises:
            None.
        """

        s = Serializer(secret_key)
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return user_id
