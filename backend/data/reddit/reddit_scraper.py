import praw
import pandas
import os
import oyaml as yaml
from bs4 import BeautifulSoup
import sys
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path,'..'))
from word_processing_tools import process_string_name,sanitize_unicode

reddit = praw.Reddit(
    client_id = '2faOhLfXc89V5LJV8rDhBg',
    client_secret='Sj9lF5bAc2Fe0zDgQz3n36E9PBgAbg',
    user_agent='Reddit scraper by u/simonchan476'
)

FILE_NAME_SCRAPED=os.path.join(os.path.dirname(__file__),'reddit_threapy.xlsx')
FILE_NAME_DATAFILE = os.path.join(os.path.dirname(__file__),'datafile_reddit.yaml')
def process_string(input_string):
    return process_string_name(sanitize_unicode(input_string))
def scrape_data():
    print(reddit.read_only)
    datas=[]
    count = 0
    for submission in reddit.subreddit("therapy").top(limit=1500):
        if submission.over_18:
            continue
        title = (submission.title)
        submission_body = submission.selftext
        if submission_body.__len__() <= 10:
            continue
        score =  submission.score
        comment_forest = submission.comments
        top_comment=''
        try:
            top_comment_html = comment_forest[0].body_html
            top_comment = ''.join(BeautifulSoup(top_comment_html).findAll(text=True))
        except Exception as e:
            continue
            pass
        datas.append([title,submission_body,score,top_comment])
        count+=1
        print(count)
    df1 = pandas.DataFrame(datas,columns=['title','submission_body','score','top_comment'])
    df1.to_excel(FILE_NAME_SCRAPED)

def process_data():
    with open(FILE_NAME_DATAFILE, 'w', encoding='utf-8') as yamlfile:
        df1 = pandas.read_excel(FILE_NAME_SCRAPED)
        data_obj = {'version':'3.0','stories':[]}
        for index,row in df1.iterrows():
            MAX_CONTENT_LENGTH=300
            if row['submission_body'].__len__() >= MAX_CONTENT_LENGTH or row['top_comment'].__len__()>= MAX_CONTENT_LENGTH:
                continue
               
            steps=[{'user': process_string(row['submission_body'])},{'bot': process_string(row['top_comment'])}] 
            data_obj['stories'].append({'story': process_string(row['title']), 'steps':steps})
            pass
        yaml.dump(data_obj,yamlfile,allow_unicode=True)
if __name__== '__main__':
    #scrape_data()
    process_data()
