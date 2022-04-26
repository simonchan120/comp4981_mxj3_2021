import nltk
from nltk.tag import StanfordNERTagger
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)
#os.environ['JAVA_HOME']=os.environ['JAVAHOME']='C:\\Program Files\\Java\\jdk-18.0.1'

#jar = 'E:\\Users\\2ndble\\ust\fyp\codebase\backend\data\standfordpostagger\stanford-postagger-full-2020-11-17\stanford-postagger-4.2.0.jar'
jar  =os.path.join(dir_path,'standfordpostagger\\stanford-ner-2020-11-17\\stanford-ner.jar')
model =os.path.join(dir_path,'standfordpostagger\\stanford-ner-2020-11-17\\classifiers\\english.all.3class.distsim.crf.ser.gz')

st = StanfordNERTagger(model,jar,encoding='utf8')
def sanitize_unicode(input_string):
    return input_string.replace(u"\u2019","'").replace('\n','').replace(u"\u2018","'")

def process_string_name(text):
    text_copy=text
    for sent in nltk.sent_tokenize(text):
        tokens = nltk.tokenize.word_tokenize(sent)
        #print(len(tokens))
        tags = st.tag(tokens)
        #print(tags)
        for tag in tags:
            if tag[1]=='PERSON': 
                print(f' replacing {tag[0]}')
                text_copy = text_copy.replace(tag[0],'you')
                print(text_copy)
    return text_copy
if __name__== '__main__':
    new_string = process_string_name('hi Simon')
    print(new_string)