from .. import tests
from backend.models import goemotions as ge, emotion_tags
import pytest

@pytest.fixture(scope="module")
def goemotions():
    return ge

@pytest.mark.parametrize('message',[('hi'),('🙃'),('😭'),('')])
def test_goemotions(message,goemotions):
    res  = goemotions(message)
    assert len(res) == 1
    print(res)
    #unpack
    res = res[0]
    assert all(label in emotion_tags for label in res['labels'])
    assert all (0<=score and score<=1  for score in res['scores']  )