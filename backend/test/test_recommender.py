import pytest
from mongoengine import *
import sys
sys.path.append("..")
import recommender
import logging
from pathlib import Path
from datetime import datetime
connect(host='mongodb://localhost:27017/test')
logger = logging.getLogger(__name__)
Path("./logs").mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=f"{datetime.now().strftime('./logs/%Y%m%d-%H%M%S')}.log",
    format='%(asctime)s %(name)s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')
def test_recommender():
    logger.debug("tes")
    content,pred_preferences = recommender.Recommender.recommend(username="1")

    logger.debug(pred_preferences)

    print("Scores:\n")
    for pref in pred_preferences:
        print(f"{pref.score}: {pref.content.name}") 
    print(f"Content:\t: {content.name}")
    pass
