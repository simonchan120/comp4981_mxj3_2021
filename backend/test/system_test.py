import sys
sys.path.append("../..")

import pytest
import random
from backend import app
import string
import requests
HOSTNAME_FLASK='http://localhost:5000'
TEST_EMAIL='ccysimon476@gmail.com'
RASA_ACCESS_TOKEN_HEADER='rasa-access-token'
@pytest.fixture()
def client():
    return requests.session()
class TestGroup:


    def test_connection(self,client):
        r = client.get(f"{HOSTNAME_FLASK}/")
        assert r.status_code == 200
    def test_register_new_user(self,client):
        TestGroup.name = 'testuser_'+''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        TestGroup.password=''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        r = client.post(f"{HOSTNAME_FLASK}/signup",data={'username':TestGroup.name,'email':TEST_EMAIL,'password':TestGroup.password})
        
        assert r.status_code == 201

    def test_new_user_email_verification(self,client,pytestconfig):
        
        capmanager = pytestconfig.pluginmanager.getplugin('capturemanager')
        capmanager.suspend_global_capture(in_=True)
        i = input("OTP for test user")
        capmanager.resume_global_capture()
        
        r = client.post(f"{HOSTNAME_FLASK}/signup/verification",data={'email':TEST_EMAIL,'otp':i})
        assert r.status_code == 200

    def test_new_user_login(self,client):
        r = client.post(f"{HOSTNAME_FLASK}/login",data={'username':TestGroup.name,'password':TestGroup.password})
        assert r.status_code == 200
        TestGroup.rasa_access_token = r.json()[RASA_ACCESS_TOKEN_HEADER]
        TestGroup.auth = {RASA_ACCESS_TOKEN_HEADER:TestGroup.rasa_access_token}
    
    def test_user_conversation(self,client):
        r = client.post(f"{HOSTNAME_FLASK}/",data={'message':'hi'},headers=TestGroup.auth)
        assert r.status_code ==200

    def test_start_new_chat_session(self,client):
        r = client.post(f"{HOSTNAME_FLASK}/new-chat-session",headers=TestGroup.auth)
        assert r.status_code == 200
        
    def test_get_user_profile(self,client):
        r = client.get(f"{HOSTNAME_FLASK}/show-profile",headers=TestGroup.auth)
        assert r.status_code == 200

    def test_add_preferences(self,client):
        r = client.post(f"{HOSTNAME_FLASK}/add-preference",headers=TestGroup.auth,data={'name':'cute','score':0.5})
        assert r.status_code == 200 

    def test_add_survey_data(self,client):
        r = client.post(f"{HOSTNAME_FLASK}/add-survey-results",headers=TestGroup.auth,data={'field_1':'1','field_2':'2','field_3':'3','field_4':'3','field_5':'5','field_6':'4','field_7':'1'})
        assert r.status_code == 200 
    def test_check_do_survey(self,client):
        r = client.get(f"{HOSTNAME_FLASK}/check-do-survey",headers=TestGroup.auth)
        assert r.status_code == 200
        assert r.json()['result'] == False
    def test_check_push_notification(self,client):
        r = client.get(f"{HOSTNAME_FLASK}/check-send-push-notification",headers=TestGroup.auth)
        assert r.status_code == 200
        assert r.json()['result'] == True
        
    def test_new_chat_session(self,client):
        r = client.post(f"{HOSTNAME_FLASK}/new-chat-session",headers=TestGroup.auth)
        assert r.status_code == 200
    def test_resend_verification_email(self,client):
        r = client.post(f"{HOSTNAME_FLASK}/signup/resend-verification-email",data = {'email':TEST_EMAIL})
        assert r.status_code == 200

    def test_cleanup(self,client):
        if TestGroup.auth is not None:
            r = client.delete(f"{HOSTNAME_FLASK}/delete-profile",headers=TestGroup.auth)
            print(r.status_code)
            assert r.status_code == 200
        assert True
        



