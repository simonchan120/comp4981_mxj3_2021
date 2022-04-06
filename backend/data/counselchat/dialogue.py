import json

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