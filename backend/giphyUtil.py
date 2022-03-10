import http.client
from json import JSONDecodeError
import logging
from random import randint, choice
#from flask import current_app
import requests
import re
from .recommender import Recommender

logger = logging.getLogger(__name__)

class GiphyUtil():
    def __init__(self,api_key=None):
        self._api_key=api_key
        
    def fetch_multimedia(self,giphy_tag):
        # multimedia,_ = Recommender.recommend(user)
        # giphy_tag = multimedia.name
        giphy_links = self._fetch_giphy(giphy_tag)
        return choice(giphy_links),giphy_tag
    def _fetch_giphy(self,query):
        LINK='http://api.giphy.com/v1/gifs/search'

        r = requests.get(LINK,params={'api_key':self._api_key,'q':query})
        try:
            res = r.json()
        except JSONDecodeError as e:
            logger.exception('Failed to fetch link from giphy server')
            return []
        except Exception as e:
            logger.exception('An exception occured')
            return []
        new_list = []
        return list(map(lambda x:f"https://i.giphy.com/media/{(x['id'])}/giphy.gif",res['data']))
        for gif in res:
            #identifier = re.search("(?<=http:\/\/giphy.com\/gifs\/)[0-9A-Za-z-]*",gif.url)
            new_link = f"https://i.giphy.com/media/{identifier}/giphy.gif"