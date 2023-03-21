from application.app import create_app
from restapis.sign_up_api import SignUpAPI

app = create_app()

app.add_url_rule("/signup", view_func=SignUpAPI.as_view("sign_up_api"))


if __name__ == "__main__":
    app.run()