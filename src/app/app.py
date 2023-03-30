import os
from flask import Flask, session, g

from config.config import get_server_config, BaseConfig, DevConfig, ProdConfig, TEMPLATE_FOLDER, STATIC_FOLDER, get_env
from database.pgsql import session
from utils.logger import config_root_logger


def create_app() -> Flask:
    '''
    Creates a pre-configured Flask application.
    
    '''
    return _create_app(ProdConfig if get_env() == 'prod' else DevConfig,
                    template_folder=TEMPLATE_FOLDER,
                    static_folder=STATIC_FOLDER,)


def _create_app(config_object: BaseConfig, **kwargs) -> Flask:
    """Creates a Flask application.

    :param object config_object: The config class to use.
    :param dict kwargs: Extra kwargs to pass to the Flask constructor.
    """
    app = Flask(__name__,**kwargs)
    configure_app(app,config_object)
    return app


def configure_app(app: Flask, config_object: BaseConfig) -> None:
    
    app.config.from_object(config_object)
    
    configure_logger()  # Configure the logger

    @app.before_request
    def before_request():
        session.permanent = True    # Set new session to use
        session.modified = True     # reset the session timer on each new request

        # Create Session of the SQL Alchemy engine
        g.session = session()
    
    #@app.after_request
    #def after_request(response):
    #    print("After response")
    
    
        
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        session = g.pop('session', None)
        if session is not None:
            session.close()

def configure_logger():
    server_config = get_server_config()

    log_dir = server_config.get('logFileDir')
    if os.path.exists(log_dir) == False:
        print("Log file dirctory " + log_dir +
              " does not exist. Exiting the application...")
        exit(-1)

    print("Log file directory ==> " + log_dir)
    config_root_logger(log_dir + "/app.log")
