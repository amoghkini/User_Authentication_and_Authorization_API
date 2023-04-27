from restapis import admin_api, home_api, index_api, login_api, logout_api, password_change, password_reset, password_reset_request, sign_up_api, verify_api

def register_ruls(app):
    app.add_url_rule("/", view_func= index_api.IndexAPI.as_view("index_api"))
    app.add_url_rule("/admin", view_func=admin_api.AdminAPI.as_view("admin_api"))
    app.add_url_rule("/home", view_func=home_api.HomeAPI.as_view("home_api"))
    app.add_url_rule("/login", view_func=login_api.LoginAPI.as_view("login_api"))
    app.add_url_rule("/logout", view_func=logout_api.LogoutAPI.as_view("logout_api"))
    app.add_url_rule("/password-change",view_func= password_change.PasswordChangeAPI.as_view("password_change_api"))
    app.add_url_rule("/password-reset/<token>", view_func= password_reset.PasswordResetAPI.as_view("password_reset_api"))
    app.add_url_rule("/password-reset-request",view_func= password_reset_request.PasswordRestRequestAPI.as_view("password_reset_request_api"))
    app.add_url_rule("/signup", view_func=sign_up_api.SignUpAPI.as_view("sign_up_api"))
    app.add_url_rule("/verify/<token>", view_func=verify_api.VerifyUserAPI.as_view("verify_email_api"))
    
    return app