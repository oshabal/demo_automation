import pytest
import json
from faker import Faker
from packages.zerolens_ui.base import *

@pytest.fixture
def fake_data():
    return Faker()

@pytest.fixture(scope='session')
def browser_configuration():
    with open('./tests/browser_configuration.json') as config_file:
        data = json.load(config_file)
    return data

@pytest.fixture()
def browser_context_args(browser_context_args, browser_configuration):
    return {
        **browser_context_args,
        **browser_configuration,
        }

@pytest.fixture
def path(page):
    return Path(page)

@pytest.fixture
def packshot_generator(page):
    return Packshot_Generator(page)
