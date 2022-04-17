import sys

from backend.server import new_chat_session
#sys.path.append("../")

from .. import tests
import pytest
import random
from backend import app
import string
import requests
import numbers
from collections import Counter

HOSTNAME_FLASK=tests.HOSTNAME_FLASK
TEST_EMAIL=tests.TEST_EMAIL
RASA_ACCESS_TOKEN_HEADER=tests.RASA_ACCESS_TOKEN_HEADER
@pytest.fixture()
def client():
    return requests.session()
def id_simple_strings(val):
    if isinstance(val, (string, numbers.Number, bool)):
        return str(val)
class TestGroup:
    def get_user_profile(self,client):
        return client.get(f"{HOSTNAME_FLASK}/show-profile",headers=TestGroup.auth)

    def test_connection(self,client):
        r = client.get(f"{HOSTNAME_FLASK}/")
        assert r.status_code == 200
    def test_register_new_user(self,client):
        TestGroup.name = 'testuser_'+''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        TestGroup.password=''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        r = client.post(f"{HOSTNAME_FLASK}/signup",data={'username':TestGroup.name,'email':TEST_EMAIL,'password':TestGroup.password})
        
        assert r.status_code == 201
    
    @pytest.mark.parametrize('status_code',[200,404],ids=['first_time_input_success','wrong_otp'])
    def test_new_user_email_verification(self,client,pytestconfig,status_code):
        
        capmanager = pytestconfig.pluginmanager.getplugin('capturemanager')
        capmanager.suspend_global_capture(in_=True)
        i = input(f"\nInput OTP for test user, status_code {status_code}:\n")
        capmanager.resume_global_capture()
        
        r = client.post(f"{HOSTNAME_FLASK}/signup/verification",data={'email':TEST_EMAIL,'otp':i})
        assert r.status_code == status_code

    @pytest.fixture(scope="function")
    def username(self,request):
        value = request.param
        if value is True:
            return TestGroup.name
        elif value is False:
            return TestGroup.name + 'a'
        elif value is None:
            return None

    @pytest.fixture(scope="function")
    def password(self,request):
        value = request.param
        if value is True:
            return TestGroup.password
        elif value is False:
            return TestGroup.password + 'a'
        elif value is None:
            return None
    @pytest.mark.parametrize('username,password,status_code',
    [(True,True,200),(True,True,200),(True,False,401),(False,True,401),(None,None,401),(True,None,401),(None,True,401)]
    ,ids =['success_first','success_second','wrong_password','wrong_username','missing_both','missing_pass','missing_username'],indirect=['username','password'])
    def test_new_user_login(self,client,username,password,status_code):
        data_package = {}
        if username is not None:
            data_package['username']=username
        if password is not None:
            data_package['password']=password
        r = client.post(f"{HOSTNAME_FLASK}/login",data=data_package)
        assert r.status_code == status_code
        if r.status_code == 200:
            TestGroup.name = username
            TestGroup.password= password
            TestGroup.rasa_access_token = r.json()[RASA_ACCESS_TOKEN_HEADER]
            TestGroup.auth = {RASA_ACCESS_TOKEN_HEADER:TestGroup.rasa_access_token}
    
    @pytest.mark.parametrize('message',['hi','hi2','hi3','qwerqrweqrwe14134431'],ids=['first_message','second_message','third_message','fourth_message'])
    def test_user_conversation(self,client,message):
        r = client.post(f"{HOSTNAME_FLASK}/",data={'message':message},headers=TestGroup.auth)
        assert r.status_code ==200

    def test_check_push_notification(self,client):
        r = client.get(f"{HOSTNAME_FLASK}/check-send-push-notification",headers=TestGroup.auth)
        assert r.status_code == 200
        assert r.json()['result'] == False

    def test_start_new_chat_session(self,client):
        r = client.post(f"{HOSTNAME_FLASK}/new-chat-session",headers=TestGroup.auth)
        assert r.status_code == 200
        
    def test_get_user_profile(self,client):
        r = client.get(f"{HOSTNAME_FLASK}/show-profile",headers=TestGroup.auth)
        assert r.status_code == 200
        assert r.json()['username']==TestGroup.name
        assert r.json()['email']==TEST_EMAIL

    preference_testdata = [('cute',0.5,200),('fun',1.0,200),('cute',0.6,200),('non_tag',0.6,404),('cute','notavalue',404),('cute',None,404),(None,0.5,404)]
    @pytest.mark.parametrize("name,score,status_code",preference_testdata, ids=['success_tag1','success_tag2','duplicate_success_tag1','non_existant_tag','non_money_score','missing score','missing tag'])
    def test_add_preferences(self,client,name,score,status_code):

        data_package={}
        if name is not None:
            data_package['name']=name
        if score is not None:
            data_package['score']= score
        r = client.post(f"{HOSTNAME_FLASK}/add-preference",headers=TestGroup.auth,data=data_package)
        assert r.status_code == status_code
        if r.status_code == 200:
            r = client.get(f"{HOSTNAME_FLASK}/show-profile",headers=TestGroup.auth)
            assert r.status_code == 200
            preference_object_json = next(x for x in r.json()['preferences'] if x['content']['name'] == name)
            assert preference_object_json['score'] == score

    def test_preferences_count(self,client):
        r = client.get(f"{HOSTNAME_FLASK}/show-profile",headers=TestGroup.auth)
        unique_preferences = Counter([x[0] for x in self.preference_testdata if x[0] and 'non' not in x[0]]).keys()
        database_preferences = Counter(map(lambda x: x['content']['name'],r.json()['preferences'])).keys()
        assert database_preferences==unique_preferences

    @pytest.mark.parametrize('survey_value_list,status_code',[([1,2,3,4,5,4,3,2,1],200),([1,2,3,'4',5,4,3,'2',1],200),([None,2,3,None,5,4,3,2,1],404),([1,2,3,'aweg',5,4,3,2,1],404)],ids=['normal values1','normal values2','Missing fields','non-integer values'])
    def test_add_survey_data(self,client,survey_value_list,status_code):
        data_package={}
        for idx,val in enumerate(survey_value_list):
            if val is not None:
                data_package[f'field_{idx+1}']=val
        r = client.post(f"{HOSTNAME_FLASK}/add-survey-results",headers=TestGroup.auth,data=data_package)
        assert r.status_code == status_code 
    def test_check_do_survey(self,client):
        r = client.get(f"{HOSTNAME_FLASK}/check-do-survey",headers=TestGroup.auth)
        assert r.status_code == 200
        assert r.json()['result'] == False

   

    new_chat_session_test_data=[200,200,200]
    @pytest.mark.parametrize('status_code',new_chat_session_test_data,ids = ['newchat1','newchat2','newchat3'])
    def test_new_chat_session(self,client,status_code):
        r = client.post(f"{HOSTNAME_FLASK}/new-chat-session",headers=TestGroup.auth)
        assert r.status_code == status_code

    def count_new_chats(self,client):
        r = self.get_user_profile()
        assert len(r.json['conversations']) - 1 == len(new_chat_session)

    def test_resend_verification_email(self,client):
        r = client.post(f"{HOSTNAME_FLASK}/signup/resend-verification-email",data = {'email':TEST_EMAIL})
        assert r.status_code == 200
    
    @pytest.mark.parametrize('status_code',[200,404],ids=['first_time_input_success','wrong_otp'])
    def test_user_email_verification_resent(self,client,pytestconfig,status_code):
        capmanager = pytestconfig.pluginmanager.getplugin('capturemanager')
        capmanager.suspend_global_capture(in_=True)
        i = input(f"\nInput OTP for test user, status_code {status_code}:\n")
        capmanager.resume_global_capture()
        r = client.post(f"{HOSTNAME_FLASK}/signup/verification",data={'email':TEST_EMAIL,'otp':i})
        assert r.status_code == status_code

        if status_code == 200:
            r = client.post(f"{HOSTNAME_FLASK}/login",data={'username':TestGroup.name,'password':TestGroup.password})
            assert r.status_code == status_code
    
    @pytest.mark.parametrize('message',['hi'],ids=['first_message'])
    def test_user_conversation_after_many_operations(self,client,message):
        r = client.post(f"{HOSTNAME_FLASK}/",data={'message':message},headers=TestGroup.auth)
        assert r.status_code ==200

    def test_cleanup(self,client):
        if TestGroup.auth is not None:
            r = client.delete(f"{HOSTNAME_FLASK}/delete-profile",headers=TestGroup.auth)
            print(r.status_code)
            assert r.status_code == 200
        assert True





