import json
import os 
import yaml

dir_path = os.path.dirname(os.path.realpath(__file__))
JSON_FILE  = os.path.join(dir_path,'custom.json')

RULES_FILE = os.path.join(dir_path,'rules.yml')
NLU_FILE = os.path.join(dir_path,'nlu.yml')
DOMAIN_FILE = os.path.join(dir_path,'domain.yml')
with open(JSON_FILE,'r') as f:
    data = json.load(f)

    nluymlobj = {'version': '3.0', 'nlu': []}
    rulesymlobj = {'version': '3.0','rules':[], 'stories':[]}
    domainymlobj = {'version': '3.0', 'intents':[],'responses':{}}
    for entry in data:
        name =  entry['name'] 
        response_name = f"utter_{name}"
        inputs = entry['inputs']
        responses = entry['responses']
        intent_obj = {}
        intent_obj['intent'] = name
        intent_obj['examples'] = inputs
        nluymlobj['nlu'].append(intent_obj)

        rules_obj = {}
        rules_obj['rule'] = f"Handle {name}"
        rules_obj['steps'] = [{'intent':name},{'action':response_name}]
        rulesymlobj['rules'].append(rules_obj)
        
        story_obj = {}
        story_obj['story']=f"Handle {name}"
        story_obj['steps']= [{'intent':name},{'action':response_name}]
        rulesymlobj['stories'].append(story_obj)

        domainymlobj['responses'][response_name] = [{'text': response} for response in responses]
        domainymlobj['intents'].append(response_name)

    with open(NLU_FILE, 'w') as wf:
        yaml.dump(nluymlobj, wf, sort_keys=False)
    with open(RULES_FILE, 'w') as wf:
        yaml.dump(rulesymlobj, wf, sort_keys=False)
    with open(DOMAIN_FILE, 'w') as wf:
        yaml.dump(domainymlobj, wf, sort_keys=False)                

