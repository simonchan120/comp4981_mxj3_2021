from random import random,uniform
from regex import F

from sqlalchemy import false
from backend.data import dataclass
from .. import tests
import pytest
from backend import giphyUtil, recommender
HOSTNAME_FLASK=tests.HOSTNAME_FLASK
TEST_EMAIL=tests.TEST_EMAIL
RASA_ACCESS_TOKEN_HEADER=tests.RASA_ACCESS_TOKEN_HEADER

valid_giphy_test_tags=tests.valid_giphy_test_tags

@pytest.fixture(scope="session")
def existing_multimedia():
    existing_multimedia= dataclass.MultiMediaData.objects.all()
    return existing_multimedia

@pytest.fixture(scope="session")
def create_user(existing_multimedia):
    def _make_user(name=None):
        if name is None:
            name = 'recommender_test_testuser'
        
        preferences = [dataclass.Preference(content= multimedia,score=uniform(0,1))for multimedia in existing_multimedia]
        user = dataclass.User(username=name, preferences=preferences)
        return user
    return _make_user
@pytest.fixture(scope="session")
def user(create_user):
    return create_user()

def test__knn_sim(create_user, existing_multimedia):
    user1,user2 = create_user('test_user_1'),create_user('test_user_2')
    mse = recommender.Recommender._knn_sim(user1,user2)
    assert mse <= len(existing_multimedia)

def test__predict_scores(user:dataclass.User,create_user):
    top_k_neighbors = [create_user(f'test_user_{idx}') for idx in range(0,5)]
    preference_list = recommender.Recommender._predict_scores(user,top_k_neighbors)
    existing_preferences_names = map(lambda x: x.content.name , user.preferences)
    predicted_preferences_names = map(lambda x: x.content.name , preference_list)
    assert all(x not in predicted_preferences_names for x in existing_preferences_names)

def test_recommend(user:dataclass.User, existing_multimedia):
    (content,pred_preferences)=recommender.Recommender.recommend(user,save_predicted=False)
    assert len(user.pred_preferences) >= len(user.preferences)
    assert content in existing_multimedia
