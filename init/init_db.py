
from mongoengine import connect
from backend import dataclass
import os

def init_db_multimedia_giphy():
    connect(host=os.environ['MONGO_CONNECTION_STRING'])
    GIPHY_TAGS=['fun','movies','vacation','animals','holidays','cute','happy','pets','celebrities','nature']
    existing_tags = list(map(lambda x: x.name, dataclass.MultiMediaData.objects(name__in=GIPHY_TAGS).all()))
    tags_to_be_added = list(filter(lambda tag: tag in existing_tags,GIPHY_TAGS))
    dataclass.MultiMediaData.objects.insert([dataclass.MultiMediaData(name=x,description='giphy_tag')for x in tags_to_be_added])
    
if __name__ == '__main__':
    init_db_multimedia_giphy()