import json
import socket
import http.client
import json
from data.dialogue import Sentence,Dialogue
import yaml
import datetime


from dataclass import *

import logging

logger = logging.getLogger(__name__)

class Rasa_Client():
    def __init__(self):
        
        pass
    def send_message(self,msg,username):
            self.conn = http.client.HTTPConnection("localhost",5005)
            send_msg_link = "/webhooks/rest/webhook"
            package = {}
            package['sender'] = username
            package['message'] = msg
            json_package = json.dumps(package)
            print(package['message'])
            self.conn.request("POST", send_msg_link,json_package)

            #responses are byte strings
            response = self.conn.getresponse()
            print(response.status, response.reason)
            data = response.read()
            # assuming plain json
            data = data.decode('utf-8')

            data = json.loads(data)
            text_response = print(data[0]['text'])
            data = json.dumps(data)
            return data,response.status

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