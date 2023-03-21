import os
from flask import Flask

from config.config import get_server_config
from restapis.sign_up_api import SignUpAPI
from utils.logger import config_root_logger

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'some_secret_key'

app.add_url_rule("/signup", view_func=SignUpAPI.as_view("sign_up_api"))

server_config = get_server_config()
    
log_dir = server_config.get('logFileDir')
if os.path.exists(log_dir) == False:
    print("Log file dirctory " + log_dir +
          " does not exist. Exiting the application...")
    exit(-1)

print("Log file directory ==> " + log_dir)

config_root_logger(log_dir + "/app.log")

port = server_config.get('port')


if __name__ == "__main__":
    app.run(port = port)