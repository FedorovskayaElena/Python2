from selenium import webdriver
from fixture.session import SessionHelper
from fixture.project import ProjectHelper


class Application:
    def __init__(self, browser, baseURL):
        if browser == "Firefox":
            self.wd = webdriver.Firefox(capabilities={"marionette": False},
                                        firefox_binary="/Applications/Firefox.app/Contents/MacOS/firefox")
        elif browser == "Chrome":
            self.wd = webdriver.Chrome()
        else:
            raise ValueError("Unrecognized browser %s" % browser)
        self.session = SessionHelper(self)
        self.project = ProjectHelper(self)
        # self.contact = ContactHelper(self)
        self.baseURL = baseURL

    def open_home_page(self):
        wd = self.wd
        if not (wd.current_url.endswith("/index.php") and len(wd.find_elements_by_id("LoginForm")) > 0):
            wd.get(self.baseURL)

    def destroy(self):
        self.wd.quit()

    def is_valid(self):
        try:
            self.wd.current_url
            return True
        except:
            return False
