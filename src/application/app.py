from flask import Flask, session

from config.config import BaseConfig, DevConfig, ProdConfig, PROJECT_ROOT, TEMPLATE_FOLDER, STATIC_FOLDER, get_env

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

def configure_app(app: Flask, config_object: BaseConfig):
    app.config.from_object(config_object)
    
    @app.before_request
    def before_request():
        session.permanent = True    # Set new session to use
        session.modified = True     # reset the session timer on each new request
    
    