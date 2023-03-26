from app.app import create_app
from config.config import get_server_config
from restapis import home_api, index_api, login_api, logout_api, sign_up_api

app = create_app()

app.add_url_rule("/", view_func= index_api.IndexAPI.as_view("index_api"))
app.add_url_rule("/home", view_func=home_api.HomeAPI.as_view("home_api"))
app.add_url_rule("/login", view_func=login_api.LoginAPI.as_view("login_api"))
app.add_url_rule("/logout", view_func=logout_api.LogoutAPI.as_view("logout_api"))
app.add_url_rule("/signup", view_func=sign_up_api.SignUpAPI.as_view("sign_up_api"))


server_config = get_server_config()
port = server_config.get('port')

if __name__ == "__main__":
    app.run(port=port)