import json
import socket
import http.client
import json
from data.dialogue import Sentence,Dialogue
import yaml

from mongoengine import *

from dataclass import *

import logging
#socket.getaddrinfo('localhost',5005)
conversation_id = 1

# conn = http.client.HTTPConnection("localhost",5005)
# #link_send = '/conversations/{conversation_id}/messages'
# link_send = "/"
# conn.request("GET", link_send)
# r1 = conn.getresponse()
# print(r1.status,r1.reason)

#mongodb 
connect(host='mongodb://localhost:27017/fyp')

class Rasa_Client():
    def __init__(self):
        
        pass
    def send_message(self,msg):
            self.conn = http.client.HTTPConnection("localhost",5005)
            send_msg_link = "/webhooks/rest/webhook"
            package = {}
            package['sender'] = "test_user"
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

            #print(data)
            data = json.loads(data)
            text_response = print(data[0]['text'])
            data = json.dumps(data)
            return data,response.status

    def add_training_data(self,dialogue):
        with open('rasa/domain.yml','r+') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            #data = data.items()
            for sentence in dialogue.sentences:
                if sentence.speaker == 'user':
                    if not sentence.intent in data['intents']:
                        data['intents'].append(sentence.intent)
                if sentence.speaker == 'bot':
                    #bot_response = f'utter_{sentence.intent}'
                    bot_response = sentence.intent
                    if not bot_response in data['responses']:
        
                        data['responses'].update({bot_response: []})
                    
                    text_exist = False
                    #Should i?
                    #print (type(data['responses'][bot_response]))
                    #print(data['responses'][bot_response])
                    for obj in data['responses'][bot_response]:
                        if obj['text'] == sentence.text:
                            text_exist=True
                            break
                    if not text_exist:
                        #print(data['responses'][bot_response])
                        data['responses'][bot_response].append({'text':sentence.text})
            f.seek(0)
            f.truncate(0)
            #print(data)
            yaml.dump(data,f)
        with open('rasa/data/nlu.yml','r+') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            #print(data)
            #data = data.items()
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
            #print(data)
            f.seek(0)
            f.truncate(0)
            yaml.dump(data,f)
        with open('rasa/data/stories.yml','r+') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            print(data)
            #data = data.items()
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