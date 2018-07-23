
def test_signup_new_account(app):
    username = "userkokokok"
    password = "pwd"
    app.james.james_ensure_user_exists(username, password)
