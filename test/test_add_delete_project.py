from model.project import Project
from random import choice
import pytest


def test_add_project(app, data_projects):

    #new_project = Project(name="Inherit None private stable 6", status="stable", view_status="private",
    #                      inherit=False, description="Test descriptio dkfjks slkf s dsf")

    new_project = data_projects

    old_projects_list = app.project.get_projects_list()
    print(old_projects_list)
    print("Len %s" % str(len(old_projects_list)))

    app.project.create(new_project)

    new_projects_list = app.project.get_projects_list()
    print(new_projects_list)
    print("Len %s" % str(len(new_projects_list)))

    old_projects_list.append(new_project)

    old_projects_list_cleaned = [p.clean_project() for p in old_projects_list]
    new_projects_list_cleaned = [p.clean_project() for p in new_projects_list]

    assert sorted(new_projects_list_cleaned, key=lambda p: p.pid_or_max()) == \
           sorted(old_projects_list_cleaned, key=lambda p: p.pid_or_max())


test_data = [i for i in range(1)]


@pytest.mark.parametrize("number", test_data)
def test_delete_project(app):

    #new_project = Project(name="Inherit None private stable 6", status="stable", view_status="private",
    #                      inherit=False, description="Test descriptio dkfjks slkf s dsf")

    old_projects_list = app.project.get_projects_list()
    if len(old_projects_list) == 0:
        app.project.create(Project(name="Inherit None private stable 6", status="stable", view_status="private",
                                   inherit=False, description="Test description"))
        old_projects_list = app.project.get_projects_list()
    print(old_projects_list)
    print("Len %s" % str(len(old_projects_list)))

    project_to_delete = choice(old_projects_list)
    app.project.delete_by_id(project_to_delete.pid)

    new_projects_list = app.project.get_projects_list()
    print(new_projects_list)
    print("Len %s" % str(len(new_projects_list)))

    old_projects_list.remove(project_to_delete)

    old_projects_list_cleaned = [p.clean_project() for p in old_projects_list]
    new_projects_list_cleaned = [p.clean_project() for p in new_projects_list]

    assert sorted(new_projects_list_cleaned, key=lambda p: p.pid_or_max()) == \
           sorted(old_projects_list_cleaned, key=lambda p: p.pid_or_max())

