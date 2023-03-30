from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

class UserMethods:
    
    @staticmethod
    def add_new_user():
        return
    
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
