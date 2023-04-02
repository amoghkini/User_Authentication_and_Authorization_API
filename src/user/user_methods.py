import jwt
import re
from datetime import datetime, timedelta
from flask import request, g
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from passlib.hash import sha256_crypt
from psycopg2.errorcodes import UNIQUE_VIOLATION
from psycopg2 import errors
from sqlalchemy import text
from sqlalchemy.engine.row import Row
from typing import Dict

from user.auth_token_status import AuthTokenStatus
from user.user import User
from utils.utils import Utils

class UserMethods:
    
    @staticmethod
    def sign_up_user(user: User) -> None:
        UserMethods.validate_user_sign_up(user)
        user.password = UserMethods.hash_password(user.password)
        UserMethods.add_new_user(user)
    
    @staticmethod
    def login_user(user: Dict) -> Row:
        existing_user = UserMethods.get_user(user.get('email'))
        if existing_user:
            status = UserMethods.validate_user_login(user, existing_user)
            if not status:
                return None
        else:
            return None
        return existing_user
    
    @staticmethod
    def hash_password(password: str) -> str:
        secure_password = sha256_crypt.encrypt(str(password))
        return secure_password

    @staticmethod
    def validate_user_login(user: Dict, 
                            db_user: Row) -> bool:
        if (user.get('email') == db_user[1]) and (sha256_crypt.verify(user.get('password'),db_user[3])):
            return True
        else:
            return False
    
    @staticmethod
    def validate_user_sign_up(user: User) -> None:
        # Check if user already exist
        existing_user = UserMethods.get_user(user.email)  
        if existing_user:
            raise ValueError("The username with this email address or phone is already exist. Please log in to the acount.")
    
        email_status = UserMethods.validate_email(user.email)
        if not email_status:
            raise ValueError("Please enter the valid email address.")
        
        password_status = UserMethods.validate_password(user.password)
        if not password_status:
            raise ValueError("Please enter the paswword that contains capital & small letters, numbers and characters.") 
    
    @staticmethod
    def reset_password(user: Dict) -> None:
        UserMethods.change_password(user,reset=True)
        
    @staticmethod
    def change_password(user: Dict, 
                        reset: bool = False) -> None:
        UserMethods.validate_change_password(user, reset)
        hashed_password = UserMethods.hash_password(user.get('new_password'))
        UserMethods.update_password(user.get('email'), hashed_password)

        
    @staticmethod
    def update_password(email: str, 
                        password: str) -> None:
        try:
            query = text('UPDATE backtest.users SET password= :password WHERE email_id= :email_id')
            g.session.execute(query, {'password': password, 'email_id': email})
            g.session.commit()
        except Exception as e:
            raise ValueError("Something went wrong while updating the password.")
    
    @staticmethod
    def validate_change_password(user: Dict,
                                 reset: bool) -> None:
        existing_user = UserMethods.get_user(user.get('email'))
        if not existing_user:
            raise ValueError("The username with this email address is not registered.")

        if not reset:
            password_status = UserMethods.check_if_old_and_new_password_is_same(user, existing_user)
            if password_status:
                raise ValueError("The old and new password should not be same.")
        
        password_status = UserMethods.validate_password(user.get('new_password'))
        if not password_status:
            raise ValueError("Please enter the paswword that contains capital & small letters, numbers and characters.")
    
    @staticmethod
    def check_if_old_and_new_password_is_same(user: Dict, 
                                              existing_user: Row) -> bool:
        if sha256_crypt.verify(user.get('old_password'), existing_user[3]):
            if user.get('old_password') == user.get('new_password'):
                return True
            else:
                return False
        else:
            raise ValueError("Please enter the correct old password")
    
    @staticmethod
    def get_user(email: str) -> Row:
        try:
            query = text('SELECT user_id, email_id, first_name, password, role_id  FROM backtest.users WHERE email_id = :email_id')
            result = g.session.execute(query, {'email_id': email})
            user = result.fetchone()
            return user
        
        except Exception as e:
            raise ValueError("Something went wrong while fetching the user details.")
        
    @staticmethod
    def get_user_by_username(username: str) -> bool:
        try:
            query = text('SELECT  email_id, username FROM backtest.users WHERE username = :username')
            result = g.session.execute(query, {'username': username})
            user = result.fetchone()
            if user:
                return True
            else:
                return False

        except Exception as e:
            raise ValueError("Something went wrong while checking if username is already taken.")
    
    @staticmethod
    def validate(data, regex):
        """Custom Validator"""
        return True if re.match(regex, data) else False

    @staticmethod
    def validate_password(password: str):
        """Password Validator"""
        reg = r"\b^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$\b"
        return UserMethods.validate(password, reg)

    @staticmethod
    def validate_email(email: str):
        """Email Validator"""
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return UserMethods.validate(email, regex)

    @staticmethod
    def add_new_user(user: User) -> bool:
        try:
            query = text('INSERT INTO backtest.users (first_name, last_name, email_id, password, mobile_no, account_creation_date, account_status, role_id) VALUES (:first_name, :last_name, :email_id, :password, :mobile_no, :account_creation_date, :account_status, :role_id)')
            g.session.execute(query, {'first_name': user.first_name, 'last_name': user.last_name,
                                      'email_id': user.email, 'password': user.password, 'mobile_no': user.mobile_no,
                                      'account_creation_date': user.account_creation_date, 'account_status': user.account_status,
                                      'role_id': user.role_id})
            g.session.commit()
            return True
        except errors.UniqueViolation:
            print("UNIQUE VIOLATION")
            raise ValueError("The email address or mobile number is already exist.")
            
        except errors.lookup(UNIQUE_VIOLATION):
            print("Duplicate entry")
            #g.session.rollback()
            raise ValueError("The email address or mobile number is already exist.")
            
        except Exception as e:
            raise ValueError("Something went wrong while writing the database. Please retry after sometime.")
    

    @staticmethod
    def generate_username(first_name: str,
                           last_name: str) -> str:
        """Generates a unique username based on the given first and last names.

        This function generates a username by concatenating the first 5 characters of the
        first name (lowercased), an underscore, and the first character of the last name
        (lowercased). If the resulting username is longer than 8 characters, it is truncated
        to 8 characters. If the username already exists in the database, the function modifies
        it by appending characters from the first and last names or a count at the end until
        it finds a unique username.

        Args:
            first_name : The first name of the user.
            last_name  : The last name of the user.

        Returns:
            str: A unique username based on the given first and last names.
        """
    
        '''
        username = first_name[:5].lower() + '_' + first_name[0].lower() + last_name[0].lower()
        if len(username) > 8:
            username = username[:8]
            
        '''
        # Generate the initial username
        username = f"{first_name[:5]}_{first_name[0]}{last_name[0]}".lower()
        
        # Check if the initial username already exists
        username_exists = UserMethods.get_user_by_username(username)
        
        # If the username already exists, modify it
        if username_exists:
            last_name_index = 1
            first_name_index = 0
            while username_exists:
                # If all characters of last name are used and the username still exists, reset the last name index and try using next character of first name
                if last_name_index >= len(last_name):
                    last_name_index = 0
                    first_name_index += 1
                    
                    # If all characters of first name are also used, append count to the end of username
                    if first_name_index >= len(first_name):
                        count = 1
                        while True:
                            if count > 99:
                                raise ValueError(
                                    "Could not create/ find a unique username.")
                            if count < 10:
                                modified_username = f"{username[:-1]}{count}"
                            else:
                                modified_username = f"{username[:-2]}{count}"
                            if not UserMethods.get_user_by_username(modified_username):
                                return modified_username
                            count += 1
                    else:
                        username = f"{username[:6]}{first_name[first_name_index]}{last_name[0]}"
                        first_name_index += 1
                else:
                    username = f"{username[:7]}{last_name[last_name_index]}"
                    last_name_index += 1
                username_exists = UserMethods.get_user_by_username(username)
    
        return username
    
    @staticmethod
    def logout_user() -> None:
        authorization = request.headers.get("authorization")
        if authorization:
            token = authorization.split(" ")[1]
        else:
            token = ''
            
        if token:
            query = text('INSERT INTO backtest.blacklisted_tokens (token, blacklisted_on, blacklisting_reason) VALUES (:token, :blacklisted_on, :blacklisting_reason)')
            g.session.execute(query, {'token': token, 'blacklisted_on': Utils.getEpoch(), 'blacklisting_reason': AuthTokenStatus.LOG_OUT})
            g.session.commit()     
        else:
            raise ValueError("Invalid Token")

    @staticmethod
    def generate_auth_token(user_data: Dict) -> str:
        try:
            exp_time = datetime.now() + timedelta(minutes=30)
            exp_epoch_time = int(exp_time.timestamp())
            data = {"payload": user_data,
                    "exp": exp_epoch_time
                        }
            return jwt.encode(data, "secret_key", algorithm="HS256")
        except Exception as e:
            raise ValueError("Not able to generate the authentication token")
    
    @staticmethod
    def decode_auth_token(auth_token: str) -> int:
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
    def check_if_token_is_blacklisted(auth_token: str) -> bool:
        query = text('SELECT * FROM backtest.blacklisted_tokens WHERE token = :token')
        result = g.session.execute(query, {'token': auth_token})
        response = result.fetchone()
        
        if response:
            return True
        else:
            return False
    
    @staticmethod
    def generate_token(user_id: str, 
                       secret_key: str = 'secret_key', 
                       epires_sec: int = 1000) -> str:
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
    def decode_token(token: str, 
                     secret_key: str = 'secret_key') -> str:
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
