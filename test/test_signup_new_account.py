
import random
import string


def random_username(prefix, maxlen):
    s = "".join([random.choice(string.ascii_letters) for i in range(random.randrange(maxlen))])
    return prefix + s


def test_signup_new_account(app):
    username = random_username("UUU_", 10)
    email = username + "@localhost"
    password = "test"
    app.james.james_ensure_user_exists(username, password)
    app.signup.new_user(username, email, password)
    # app.session.login(username, password)
    # assert app.session.is_logged_in_as(username)
    # app.session.logout()
    assert app.soap.can_login(username, password)