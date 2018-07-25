from model.project import Project
from random import choice
import pytest


# тест создания проекта с проверкой по soap
def test_add_project_soap(app, data_projects, login):
    new_project = data_projects
    old_projects_list = app.soap.get_projects_list(app.config["webadmin"]["user"], app.config["webadmin"]["password"])

    app.project.create(new_project)

    # если проект с таким именем уже есть, то добавиться он и не должен!
    if new_project.name in (p.name for p in old_projects_list):
        print("УЖЕ ЕСТЬ ТАКОЙ!!!")
    else:
        old_projects_list.append(new_project)

    new_projects_list = app.soap.get_projects_list(app.config["webadmin"]["user"], app.config["webadmin"]["password"])

    assert sorted(new_projects_list, key=lambda p: p.pid_or_max()) == \
           sorted(old_projects_list, key=lambda p: p.pid_or_max())


test_data = [i for i in range(3)]


# тест удаления проекта с проверкой по soap
@pytest.mark.parametrize("number", test_data)
def test_delete_project_soap(app, login, number):

    old_projects_list = app.soap.get_projects_list(app.config["webadmin"]["user"], app.config["webadmin"]["password"])
    if len(old_projects_list) == 0:
        app.project.create(Project(name="Inherit None private stable 6", status="stable", view_status="private",
                                   inherit=False, description="Test description"))
        old_projects_list = app.soap.get_projects_list(app.config["webadmin"]["user"], app.config["webadmin"]["password"])

    project_to_delete = choice(old_projects_list)
    app.project.delete_by_pid(project_to_delete.pid)

    new_projects_list = app.soap.get_projects_list(app.config["webadmin"]["user"], app.config["webadmin"]["password"])
    old_projects_list.remove(project_to_delete)

    assert sorted(new_projects_list, key=lambda p: p.pid_or_max()) == \
           sorted(old_projects_list, key=lambda p: p.pid_or_max())

