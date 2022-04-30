import json
from typing import List

class Sentence():
    def __init__(self,speaker,text,intent=None):
        self.speaker=speaker
        self.text=text
        self.intent=intent
    
class Dialogue():
    def __init__(self,sentences):
        self.sentences=[]
        for sentence in sentences:
            self.sentences.append(Sentence(**sentence))

class Scenario():
    name: str
    user_inputs: List[str]
    bot_responses: List[str]
    def __init__(self,name,user_inputs,bot_responses):
        self.name=name
        self.user_inputs = user_inputs or []
        self.bot_responses=  bot_responses or []
    def add_user_input(self,user_input: str):
        self.user_inputs.append(user_input)
    def add_bot_response(self,bot_response: str):
        self.bot_responses.append(bot_response)
class Scenarios():
    scenario_list: List[Scenario]
    def __init__(self):
        self.scenario_list = []
    def add_scenario(self,scenario_obj : Scenario):
        self.scenario_list.append(scenario_obj)
    def find_scenario(self,name):
        return next(scenario.name == name for scenario in self.scenario_list)

    