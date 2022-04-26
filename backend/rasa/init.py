import yaml
import os
with open("endpoints.yml", 'r') as f:
    y = yaml.safe_load(f)
    y['tracker_store']['db']= os.environ['MONGO_DB']
    y['tracker_store']['username']= os.environ['MONGO_USERNAME']
    y['tracker_store']['password']= os.environ['MONGO_PASSWORD']
    with open("endpoints.yml",'w') as f_w:
        yaml.dump(y,f_w)
