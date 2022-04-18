from .. import tests
import pytest
from backend import rasa,dataclass

base_create_user= tests.base_create_user
base_user = tests.base_user

@pytest.fixture(scope="session")
def rasa_client():
    return rasa.Rasa_Client('localhost')

@pytest.fixture(scope="module")
def create_user(base_create_user):
    def _create_user(*args,**kwargs):
        _user = base_create_user(*args,**kwargs)
        _user.latest_conversation_uuid = 'test_rasa_12362138602168'
        return _user
    return _create_user
@pytest.fixture(scope="module")
def user(create_user:dataclass.User):
    _user=create_user()
    return _user

@pytest.mark.parametrize('message,status_code',[('hi',200),('🙃',200),('😭',200),(',,,,,,ree,,,,,,,',200)])
def test_send_message(user:dataclass.User, message: str,status_code : int,rasa_client: rasa.Rasa_Client):
    
    res,returned_status_code = rasa_client.send_message(user,message)
    assert len(res) == 1
    assert returned_status_code == status_code
    assert  res[0]['recipient_id']== user.latest_conversation_uuid
    assert len(res[0]['text']) > 0

