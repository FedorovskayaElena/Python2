from telnetlib import Telnet


class JamesHelper:
    def __init__(self, app):
        self.app = app

    def james_ensure_user_exists(self, username, password):
        james_config = self.app.config["james"]
        session = JamesHelper.Session(james_config["host"], james_config["port"], james_config["username"], james_config["password"])
        if session.is_user_registered(username):
            session.reset_password(username, password)
            print("\nPassword reset %s/%s" % (username, password))
        else:
            session.create_user(username, password)
            print("\nUser created %s/%s" % (username, password))
        session.quit()

    class Session:
        def __init__(self, host, port, username, password):
            self.telnet = Telnet(host, port, 5)
            self.read_until("Login id:")
            self.bwrite(username + "\n")
            self.read_until("Password:")
            self.bwrite(password + "\n")
            self.read_until("Welcome root. HELP for a list of commands")

        def is_user_registered(self, username):
            self.bwrite("verify %s" % username + "\n")
            res = self.telnet.expect([b'exists', b'does not exist'])
            return res[0] == 0

        def create_user(self, username, password):
            self.bwrite("adduser %s %s" % (username, password) + "\n")
            self.read_until("User %s added" % username)

        def reset_password(self, username, password):
            self.bwrite("setpassword %s %s" % (username, password) + "\n")
            self.read_until("Password for %s reset" % username)

        def quit(self):
            self.bwrite("quit\n")

        def read_until(self, text):
            self.telnet.read_until(text.encode('ascii'), 5)

        def bwrite(self, text):
            self.telnet.write(text.encode('ascii'))
