import pytest
from fixture.application import Application
import json

import os.path
import importlib

fixture = None
target = None


def load_config(file):
    global target
    if target is None:
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        with open(config_file) as cf:
            target = json.load(cf)
    return target


# Создание фикстуры
@pytest.fixture()
def app(request):
    global fixture
    browser = request.config.getoption("--browser")
    config = load_config(request.config.getoption("--target"))
    print("\nweb:%s" % config["web"])
    print("\nwebadmin:%s" % config["webadmin"])
    print("\njames:%s" % config["james"])
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=browser, config=config)
    # fixture.session.ensure_login(config["webadmin"]["user"], config["webadmin"]["password"])
    return fixture


# Отдельная фикстура для финализации
@pytest.fixture(scope="session", autouse=True)
def stop(request):
    def fin():
        fixture.session.ensure_logout()
        fixture.destroy()
    request.addfinalizer(fin)
    return fixture


# Создание фикстуры для логина при удалении/добавлении проектов от имени администратора
@pytest.fixture()
def login(request):
    global fixture
    print("\n\nLOGIN!!!\n\n")
    fixture.session.ensure_login(fixture.config["webadmin"]["user"], fixture.config["webadmin"]["password"])
    # def fin():
    #     fixture.session.ensure_logout()
    # request.addfinalizer(fin)
    return fixture

# # Создание фикстуры для логина при удалении/добавлении проектов от имени администратора
# @pytest.fixture(scope="function", autouse=True)
# def logout(request):
#     def fin():
#         fixture.session.ensure_logout()
#     request.addfinalizer(fin)
#     return fixture

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="Firefox")
    parser.addoption("--target", action="store", default="target.json")


def pytest_generate_tests(metafunc):
    for fixture in metafunc.fixturenames:
        if fixture.startswith("data_"):
            testdata = load_from_module(fixture[5:])
            metafunc.parametrize(fixture, testdata, ids=[str(x) for x in testdata])


def load_from_module(module):
    return importlib.import_module("data.%s" % module).testdata


