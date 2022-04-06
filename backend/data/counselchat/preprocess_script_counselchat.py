import csv
from bs4 import BeautifulSoup
from html.parser import HTMLParser
import unicodedata
import oyaml as yaml
import os
import traceback
import sys
from nltk import tokenize
#import nltk
#nltk.download('punkt')

#csv.field_size_limit(sys.maxsize)
def sanitize_unicode(str):
    #quoted_line = str.replace(u"\u2018", "'").replace(u"\u2019", "'")
    #return bytes(quoted_line, 'utf-8').decode('utf-8','ignore')
    #new_str = str.replace(u"\u2019", u"\u0060").replace("''","'")
    new_str = str.replace("''","'")
    return new_str
    return bytes(str,"utf-8").decode('utf-8').replace(u"\u2019", u"\u0060")
def post_process(str):
    return str.replace("''","'")

# to_test="Sounds like you are stuck in a cycle of hearing your ex say you don''t matter"
# print(post_process(to_test))
# exit(0)
class OParser(HTMLParser):
    def __init__(self):
        self._data=[]   
        super().__init__()
    def handle_starttag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        pass
    def handle_data(self,data):
        normalized = unicodedata.normalize("NFKD",data)
        whitespace_processed = " ".join(normalized.split())
        unicode_processed=sanitize_unicode(whitespace_processed)
        self._data.append(unicode_processed)
        #return data
file_name = os.path.join(os.path.dirname(__file__),'datafile.yaml')

length_statistics= {'over_1000':0}
def update_length_statistics(bot_reply):
    bot_reply = " ".join(answer)

    dict_key = f'{bot_reply.__len__()}'
    if dict_key in length_statistics:
        length_statistics[dict_key]=length_statistics[dict_key]+1
    else:
        length_statistics[dict_key]=1
    if bot_reply.__len__() >=1000:
        length_statistics['over_1000']=length_statistics['over_1000']+1

def entry_filter(title,question,answer):

    threshold=300
    new_title = title
    question = tokenize.sent_tokenize(question)
    answer =tokenize.sent_tokenize(answer)
    new_question=[]
    new_answer= []
    is_skip=False


    total_length_answer = 0
    for sentence in answer:
        total_length_answer = total_length_answer + sentence.__len__()
        if total_length_answer>=threshold:
            break
        new_answer.append(sentence)

    total_length_question = 0
    for sentence in question:
        total_length_question = total_length_question + sentence.__len__()
        if total_length_question>=threshold:
            break
        new_question.append(sentence)

    if title.__len__() <=5 or " ".join(new_question).__len__() <=5 or " ".join(new_answer).__len__() <=5:
        is_skip=True

    new_question = post_process(" ".join(new_question))
    new_answer=  post_process(" ".join(new_answer))
    return new_title,new_question,new_answer,is_skip
with open(file_name, 'w', encoding='utf-8') as yamlfile:
    data_obj = {'version':'3.0','stories':[]}
    with open(os.path.join(os.path.dirname(__file__),'counselchat-data-1.csv'),newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile,delimiter=',',quotechar='"')
        title_index = 1
        question_index = 2
        for idx,row in enumerate(reader):
            if idx == 0:
                continue
            parser = OParser()
            #print(f"{idx}:\t{row}\n")
            #soup = BeautifulSoup(row[-2], "html.parser")
            #page = soup.find('p').getText()
            parser.feed(row[-2])
            
            try:
                # if idx == 50:
                #     break
                title = sanitize_unicode(unicodedata.normalize("NFKD",row[title_index]))
                question = " ".join(sanitize_unicode(unicodedata.normalize("NFKD",row[question_index])).split())
                answer = " ".join(parser._data)
                print(f"{idx}:\nTitle:{title}\nQuestion:{question}\nAnswer:{row[-2]}\t{answer}")
                #bot_reply = [{'bot':bot_reply_sentence} for bot_reply_sentence in answer]
                #steps = [{'user': question}] + bot_reply + [{'user': 'thanks'}, {'bot':'talking to you was nice'}]
                
                update_length_statistics(answer)
                
                title,question,answer,is_skip = entry_filter(title,question,answer)
                if is_skip:
                    continue

                print(answer)
                steps = [{'user': question}] + [{'bot': answer}] 
                data_obj['stories'].append({'story': title, 'steps':steps})
            except Exception as e:
                print(traceback.print_exc())
                print(f"ERROR\t{idx}")
                #print(f":\t{row[-2]}\t")
            #print(f"{idx}:\t{row[title_index]}\t{row[question_index]}\t{data}")

    #yaml.dump(data_obj,yamlfile,width=float("inf"),allow_unicode=True)
    yaml.dump(data_obj,yamlfile,allow_unicode=True)
    length_statistics['less_1000']=length_statistics.__len__()-length_statistics['over_1000']
    print(length_statistics)
    