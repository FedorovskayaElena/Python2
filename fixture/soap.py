from suds.client import Client
from suds import WebFault
from model.project import Project


class SoapHelper:

    def __init__(self, app):
        self.app = app

    def can_login(self, username, password):
        client = Client("http://localhost/mantisbt-1.2.20/api/soap/mantisconnect.php?wsdl")
        try:
            client.service.mc_login(username, password)
            return True
        except WebFault:
            return False

    def get_projects_list(self, username, password):
        client = Client("http://localhost/mantisbt-1.2.20/api/soap/mantisconnect.php?wsdl")
        try:
            data = client.service.mc_projects_get_user_accessible(username, password)
            projects_list = []
            for p in data:
                projects_list.append(Project(pid=p["id"], name=p["name"], status=p["status"]["name"],
                                             view_status=p["view_state"]["name"], description=p["description"]))
            return projects_list
        except WebFault:
            return False

