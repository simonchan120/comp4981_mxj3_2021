#https://stackoverflow.com/questions/25827160/importing-correctly-with-pytest
import os
from mongoengine import connect
GIPHY_API_KEY = os.environ['GIPHY_API_KEY']
HOSTNAME_FLASK='http://localhost:5000'
TEST_EMAIL='ccysimon476@gmail.com'
RASA_ACCESS_TOKEN_HEADER='rasa-access-token'
MONGO_CONNECTION_STRING=os.environ['MONGO_CONNECTION_STRING']
valid_giphy_test_tags=['cute','vacation','funny']

connect(host=MONGO_CONNECTION_STRING)
