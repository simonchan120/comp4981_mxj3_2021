#https://stackoverflow.com/questions/25827160/importing-correctly-with-pytest
import os
from mongoengine import connect
from backend import dataclass
import pytest
from random import uniform,random, choices
import string
GIPHY_API_KEY = os.environ['GIPHY_API_KEY']
HOSTNAME_FLASK='http://localhost:5000'
TEST_EMAIL='ccysimon476@gmail.com'
RASA_ACCESS_TOKEN_HEADER='rasa-access-token'
MONGO_CONNECTION_STRING=os.environ['MONGO_CONNECTION_STRING']
valid_giphy_test_tags=['cute','vacation','funny']

connect(host=MONGO_CONNECTION_STRING)



@pytest.fixture(scope="session")
def base_create_user():
    existing_names = []
    def _make_user(name=None):
        while True:
            if name is None or name in existing_names:
                rand_id=''.join(choices(string.ascii_uppercase + string.digits, k=15))
                name = f'test_testuser_{rand_id}'
            else:
                break
        user = dataclass.User(username=name)
        user.init_new_user(save_documents=False)
        return user
    return _make_user
@pytest.fixture(scope="session")
def base_user(base_create_user):
    return base_create_user()