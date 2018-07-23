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
    web = load_config(request.config.getoption("--target"))["web"]
    webadmin = load_config(request.config.getoption("--target"))["webadmin"]
    print("\nweb:%s" % web)
    print("\nwebadmin:%s" % webadmin)
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser, web["baseURL"])
    fixture.session.ensure_login(webadmin["user"], webadmin["password"])
    return fixture


# Отдельная фикстура для финализации
@pytest.fixture(scope="session", autouse=True)
def stop(request):
    def fin():
        fixture.session.ensure_logout()
        fixture.destroy()
    request.addfinalizer(fin)
    return fixture


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


