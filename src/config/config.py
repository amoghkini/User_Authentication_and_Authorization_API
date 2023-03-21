import json
import os
from datetime import timedelta
from typing import Dict

APP_NAME = 'Backtester'
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
TEMPLATE_FOLDER = os.path.join(PROJECT_ROOT, 'templates')
STATIC_FOLDER = os.path.join(PROJECT_ROOT, 'static')


def get_server_config() -> Dict:
    """
    Reads and returns the server configuration data from a JSON file located
    at '../config/serverr.json'.

    Returns:
        A dictionary object containing the server configuration data.

    Raises:
        FileNotFoundError: If the server.json file is not present in the
            config directory.
        Exception: If any other error occurs while reading the file.

    Example usage:
        >>> server_config = get_server_config()
        >>> print(server_config['logFileDir'])
        'F:/Projects/logs'
        >>> print(server_config['port'])
        5000
    """
    
    try:
        with open('../config/server.json') as server:
            json_servr_data = json.load(server)
            return json_servr_data
        
    except FileNotFoundError as e:
        print("The server.json file is not present in the config directory." \
            "Please add the valid config file.")
        exit(-1)
        
    except Exception as e:
        print("Exception occured while reading the file.")
        exit(-1)

def get_env():
    return get_server_config().get('env')

class BaseConfig(object):
    ##########################################################################
    # flask                                                                  #
    ##########################################################################
    
    DEBUG = True if get_env() == 'dev' else False
    SECRET_KEY = "THIS IS SECRET KEY"  


    ##########################################################################
    # Session                                                                #
    ##########################################################################

    PERMANENT_SESSION_LIFETIME = timedelta(minutes=60)


    ##########################################################################
    # database                                                               #
    ##########################################################################
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False




class ProdConfig(BaseConfig):
    ##########################################################################
    # flask                                                                  #
    ##########################################################################
    ENV = 'prod'
    DEBUG = True if get_env() == 'dev' else False

    ##########################################################################
    # database                                                               #
    ##########################################################################
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}'.format(
        user=os.environ.get('FLASK_DATABASE_USER', 'flask_api'),
        password=os.environ.get('FLASK_DATABASE_PASSWORD', 'flask_api'),
        host=os.environ.get('FLASK_DATABASE_HOST', '127.0.0.1'),
        port=os.environ.get('FLASK_DATABASE_PORT', 5432),
        db_name=os.environ.get('FLASK_DATABASE_NAME', 'flask_api'),
    )


class DevConfig(BaseConfig):
    ##########################################################################
    # flask                                                                  #
    ##########################################################################
    ENV = 'dev'
    DEBUG = True if get_env() == 'dev' else False

    ##########################################################################
    # database                                                               #
    ##########################################################################
    
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}'.format(
        user=os.environ.get('FLASK_DATABASE_USER', 'flask_api'),
        password=os.environ.get('FLASK_DATABASE_PASSWORD', 'flask_api'),
        host=os.environ.get('FLASK_DATABASE_HOST', '127.0.0.1'),
        port=os.environ.get('FLASK_DATABASE_PORT', 5432),
        db_name=os.environ.get('FLASK_DATABASE_NAME', 'flask_api'),
    )
