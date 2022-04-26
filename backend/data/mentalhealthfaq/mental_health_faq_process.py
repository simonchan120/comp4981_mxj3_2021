import praw
import pandas
import os
import oyaml as yaml
from bs4 import BeautifulSoup
import nltk
from nltk.tag import StanfordPOSTagger
import sys
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path,'..'))
from word_processing_tools import process_string_name,sanitize_unicode

FILE_NAME_CSV=os.path.join(os.path.dirname(__file__),'Mental_Health_FAQ.csv')
FILE_NAME_DATAFILE= os.path.join(os.path.dirname(__file__),'datafile_mental_health_faq.yaml')

def preprocess_data(text):
    #return process_string_name(sanitize_unicode(text))
    return sanitize_unicode(text)
def process_data():
    with open(FILE_NAME_DATAFILE, 'w', encoding='utf-8') as yamlfile:
        df1 = pandas.read_csv(FILE_NAME_CSV)
        data_obj = {'version':'3.0','stories':[]}
        for index,row in df1.iterrows():
            MAX_CONTENT_LENGTH=30000
            if row['Questions'].__len__() >= MAX_CONTENT_LENGTH or row['Answers'].__len__()>= MAX_CONTENT_LENGTH:
                continue
               
            steps=[{'user': preprocess_data(row['Questions'])},{'bot': preprocess_data(row['Answers'])}] 
            data_obj['stories'].append({'story': row['Question_ID'], 'steps':steps})
            
            pass
        yaml.dump(data_obj,yamlfile,allow_unicode=True)
if __name__ == '__main__':
    process_data()