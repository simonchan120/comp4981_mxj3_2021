import json
import requests
import yaml

try:
    from .data.dataclass import *
except:
    from data.dataclass import *
import logging
logger = logging.getLogger(__name__)
#TODO: change this when delpoying
RASA_HOST_NAME= 'rasa'
class Rasa_Client():
    def __init__(self):
        

        pass
    def send_message(self,user,msg):
            session_uuid = user.latest_conversation_uuid
            r = requests.post(f'http://{RASA_HOST_NAME}:5005/webhooks/rest/webhook',json.dumps({'sender':session_uuid,'message':msg}))
            data=  r.json()
            return data,r.status_code

    def add_training_data(self,dialogue):
        with open('rasa/domain.yml','r+') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            for sentence in dialogue.sentences:
                if sentence.speaker == 'user':
                    if not sentence.intent in data['intents']:
                        data['intents'].append(sentence.intent)
                if sentence.speaker == 'bot':
                    bot_response = sentence.intent
                    if not bot_response in data['responses']:
        
                        data['responses'].update({bot_response: []})
                    
                    text_exist = False
                    #Should i?
                    for obj in data['responses'][bot_response]:
                        if obj['text'] == sentence.text:
                            text_exist=True
                            break
                    if not text_exist:
                        data['responses'][bot_response].append({'text':sentence.text})
            f.seek(0)
            f.truncate(0)
            yaml.dump(data,f)
        with open('rasa/data/nlu.yml','r+') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            for sentence in dialogue.sentences:
                if sentence.speaker == 'user':
                    intent_exist = False
                    to_modify_intent = None
                    for obj in data['nlu']:
                        if obj['intent'] == sentence.intent:
                            intent_exist=True
                            to_modify_intent = obj
                            break
                    if not intent_exist:
                        data['nlu'].append({'intent':sentence.intent,'examples':f'- {sentence.text}\n'})
                    else:
                        to_modify_intent['examples'] += f'- {sentence.text}\n'
            f.seek(0)
            f.truncate(0)
            yaml.dump(data,f)
        with open('rasa/data/stories.yml','r+') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            print(data)
            steps = []
            for sentence in dialogue.sentences:
                if sentence.speaker == 'user':
                    steps.append({'intent':sentence.intent})
                elif sentence.speaker == 'bot':
                    steps.append({'action':sentence.intent})
            
            story = {'story':'generated','steps':steps }
            data['stories'].append(story)
            print(data)
            f.seek(0)
            f.truncate(0)
            yaml.dump(data,f)
        pass