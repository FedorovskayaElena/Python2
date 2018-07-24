from selenium import webdriver
from fixture.session import SessionHelper
from fixture.project import ProjectHelper
from fixture.james import JamesHelper
from fixture.signup import SignupHelper
from fixture.mail import MailHelper
from fixture.soap import SoapHelper


class Application:
    def __init__(self, browser, config):
        if browser == "Firefox":
            self.wd = webdriver.Firefox(capabilities={"marionette": False},
                                        firefox_binary="/Applications/Firefox.app/Contents/MacOS/firefox")
        elif browser == "Chrome":
            self.wd = webdriver.Chrome()
        else:
            raise ValueError("Unrecognized browser %s" % browser)
        self.session = SessionHelper(self)
        self.project = ProjectHelper(self)
        self.james = JamesHelper(self)
        self.signup = SignupHelper(self)
        self.mail = MailHelper(self)
        self.soap = SoapHelper(self)
        # self.contact = ContactHelper(self)
        self.baseURL = config["web"]["baseURL"]
        self.config = config

    def open_home_page(self):
        wd = self.wd
        if not (wd.current_url.endswith("/login_page.php") and len(wd.find_elements_by_id("login_form")) > 0):
            wd.get(self.baseURL)

    def destroy(self):
        self.wd.quit()

    def is_valid(self):
        try:
            self.wd.current_url
            return True
        except:
            return False
