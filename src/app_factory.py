from app.app import create_app
from config.config import get_server_config
from restapis.sign_up_api import SignUpAPI

app = create_app()

app.add_url_rule("/", view_func=SignUpAPI.as_view("sign_up_api"))

server_config = get_server_config()
port = server_config.get('port')

if __name__ == "__main__":
    app.run(port=port)