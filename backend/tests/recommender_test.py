from random import random,uniform
from regex import F

from sqlalchemy import false
from backend.data import dataclass
from .. import tests
import pytest
from backend import recommender
HOSTNAME_FLASK=tests.HOSTNAME_FLASK
TEST_EMAIL=tests.TEST_EMAIL
RASA_ACCESS_TOKEN_HEADER=tests.RASA_ACCESS_TOKEN_HEADER

valid_giphy_test_tags=tests.valid_giphy_test_tags

base_create_user= tests.base_create_user
base_user = tests.base_user
from backend.models import emotion_tags

@pytest.fixture(scope="module")
def existing_multimedia():
    existing_multimedia= dataclass.MultiMediaData.objects.all()
    return existing_multimedia

@pytest.fixture(scope="module")
def create_user(base_create_user,existing_multimedia):
    def _create_user(*args,**kwargs):
        _user = base_create_user(*args,**kwargs)
        _user.preferences = [dataclass.Preference(content= multimedia,score=uniform(0,1))for multimedia in existing_multimedia]
        _user.latest_emotion_profile= recommender.Recommender.calculate_new_emotion_profile(_user,"test")
        return _user
    return _create_user


@pytest.fixture(scope="module")
def user(create_user:dataclass.User):
    _user=create_user()
    return _user


def test__knn_sim(create_user, existing_multimedia):
    user1,user2 = create_user('test_user_1'),create_user('test_user_2')
    print(user1.preferences)
    mse = recommender.Recommender._knn_sim(user1,user2)
    assert mse <= len(existing_multimedia)

def test__predict_scores(user:dataclass.User,create_user):
    top_k_neighbors = [create_user(f'test_user_{idx}') for idx in range(0,5)]
    preference_list = recommender.Recommender._predict_scores(user,top_k_neighbors)
    existing_preferences_names = map(lambda x: x.content.name , user.preferences)
    predicted_preferences_names = map(lambda x: x.content.name , preference_list)
    assert all(x not in predicted_preferences_names for x in existing_preferences_names)

def test_recommend_multimedia(user:dataclass.User, existing_multimedia):
    (content,pred_preferences)=recommender.Recommender.recommend_multimedia(user,save_user=False)
    assert len(user.pred_preferences) >= len(user.preferences)
    assert content in existing_multimedia

def test_recommend_activities(user:dataclass.User):
    emotion=recommender.Recommender.recommend_activities(user)
    assert emotion in emotion_tags
