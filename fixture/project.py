from model.project import Project
from time import sleep
from selenium.webdriver.support.ui import Select


class ProjectHelper:
    def __init__(self, app):
        self.app = app

    projects_cache = None

    def create(self, project):
        wd = self.app.wd
        self.open_projects_page()
        wd.find_element_by_xpath("//input[@value='Create New Project']").click()
        self.fill_project_fields(project)
        wd.find_element_by_xpath("//input[@value='Add Project']").click()
        self.projects_cache = None
        # self.open_projects_page()

    def open_projects_page(self):
        wd = self.app.wd
        if not (wd.current_url.endswith("/manage_proj_page.php") and
                len(wd.find_elements_by_xpath("//input[@value='Create New Project']")) > 0):
            wd.find_element_by_link_text("Manage").click()
            wd.find_element_by_link_text("Manage Projects").click()

    def fill_project_fields(self, project):
        self.type_in_field("name", project.name)
        self.select_drop_down("status", project.status)
        self.set_checkbox("inherit_global", project.inherit)
        self.select_drop_down("view_state", project.view_status)
        self.type_in_field("description", project.description)

    def select_drop_down(self, select_name, selected_value):
        wd = self.app.wd
        if selected_value is not None:
            # if not wd.find_element_by_name(select_name + selected_value).is_selected():
            select = Select(wd.find_element_by_name(select_name))
            select.select_by_visible_text(selected_value)

    def set_checkbox(self, checkbox, selected_value):
        wd = self.app.wd
        if selected_value is True:
            if not wd.find_element_by_name(checkbox).get_attribute('checked'):
                wd.find_element_by_name(checkbox).click()
        else:
            if wd.find_element_by_name(checkbox).get_attribute('checked'):
                wd.find_element_by_name(checkbox).click()

    def type_in_field(self, field_name, text):
        wd = self.app.wd
        if text is not None:
            wd.find_element_by_name(field_name).click()
            wd.find_element_by_name(field_name).clear()
            wd.find_element_by_name(field_name).send_keys(text)


    def get_projects_list(self):
        if self.projects_cache is None:
            wd = self.app.wd
            self.open_projects_page()
            self.projects_cache = []
            elements = wd.find_elements_by_xpath("//tr[contains(@class, 'row-')]")
            for i in range(1, len(elements)-2):
                name = elements[i].find_element_by_xpath("td[1]/a").get_attribute("innerText")
                status = elements[i].find_element_by_xpath("td[2]").text
                inherit = elements[i].find_element_by_xpath("td[3]").text
                view_status = elements[i].find_element_by_xpath("td[4]").text
                description = elements[i].find_element_by_xpath("td[5]").text
                link = elements[i].find_element_by_xpath("td[1]/a").get_attribute("href")
                pid = link.replace("http://localhost/mantisbt-1.2.20/manage_proj_edit_page.php?project_id=", "")
                self.projects_cache.append(Project(pid=pid, name=name, status=status, inherit=inherit,
                                                   view_status=view_status, description=description))
        return list(self.projects_cache)


    def open_project_page_by_id(self, pid):


    def delete_by_pid(self, pid):
        wd = self.app.wd
        self.open_projects_page()
        self.open_project_page_by_id(pid)
        # click Delete button
        wd.find_element_by_xpath("//input[@value='Delete group(s)']").click()
        self.group_cache = None
        self.open_groups_page()