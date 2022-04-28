from flask_mail import Mail
from logging.config import dictConfig
from pathlib import Path
from flask import Flask
from datetime import datetime
import json
from mongoengine import connect
import pyotp
import boto3
from botocore.config import Config
import os
from flask_cors import CORS

LOGGING_FOLDER = "backend/logs"
Path(f"{LOGGING_FOLDER}").mkdir(parents=True, exist_ok=True)
IS_DEV = 'FLASK_ENV' in os.environ and os.environ['FLASK_ENV']=='development'
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(module)s %(filename)s %(levelname)-8s %(message)s',
    }},
    'handlers': {'file': {
        'class': 'logging.handlers.RotatingFileHandler',
        'filename': f"{datetime.now().strftime(f'{LOGGING_FOLDER}/%Y%m%d-%H%M%S')}.log",
        'formatter': 'default',
    },
    'default':{
            'level': 'DEBUG' if IS_DEV else 'INFO',
            'formatter': 'default',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',  # Default is stderr
    }
    },
    'root': {
        'level': 'DEBUG' if IS_DEV else 'INFO',
        'handlers': ['default']
    }
})
app = Flask(__name__)
CORS(app)
app.config['FLASK_ENV'] = 'development' if IS_DEV else 'production'

if app.config['FLASK_ENV'] == 'development':
# TODO: change this secret key before deployment

    app.config.update(SURVEY_INTERVAL_BASE=60)
    app.config.update(SURVEY_INTERVAL_CHANGE=60)
    app.config.update(NOTIFICATION_INTERVAL=60)
    app.config.update(RUN_CALCULATE_GLOBAL_STATISTICS_PERIOD=60*1)
    app.config.update(SAVE_COPY_USERS_EMOTION_PROFILE_PERIOD=60*1)
    app.config.update(MAIL_USERNAME=os.environ['MAIL_USERNAME'])
    app.config.update(MAIL_PASSWORD=os.environ['MAIL_PASSWORD'])
    app.config.update(CELERY_RESULT_BACKEND=os.environ['MONGO_CONNECTION_STRING'])
    app.config.update(SECRET_KEY=os.environ['SECRET_KEY'])
    app.config.update(MONGO_CONNECTION_STRING=os.environ['MONGO_CONNECTION_STRING'])
    app.config.update(OTP_SECRET_KEY=os.environ['OTP_SECRET_KEY'])
    app.config.update(CELERY_BROKER_URL=os.environ['CELERY_BROKER_URL'])
    app.config.update(GIPHY_API_KEY=os.environ['GIPHY_API_KEY'])
else:
    my_config = Config(
        region_name = 'ap-east-1',
        signature_version = 's3v4',
        retries = {
            'max_attempts': 10,
            'mode': 'standard'
        }
    )
    ssm = boto3.client('ssm',config=my_config)
    app.config.update(dict(
        SECRET_KEY=os.environ['SECRET_KEY'],
        MONGO_CONNECTION_STRING=os.environ['MONGO_CONNECTION_STRING'],
        OTP_SECRET_KEY=os.environ['OTP_SECRET_KEY'],
        MAIL_USERNAME = os.environ['MAIL_USERNAME'],
        MAIL_PASSWORD = os.environ['MAIL_PASSWORD'],
        #CELERY_RESULT_BACKEND = ssm.get_parameter(Name='/mail_username', WithDecryption=True),
        CELERY_BROKER_URL = os.environ['CELERY_BROKER_URL'],
        GIPHY_API_KEY = os.environ['GIPHY_API_KEY'],

        # SECRET_KEY=ssm.get_parameter(Name='secret_key', WithDecryption=True),
        # MONGO_CONNECTION_STRING=ssm.get_parameter(Name='mongo_connection_string', WithDecryption=True),
        # OTP_SECRET_KEY=ssm.get_parameter(Name='otp_secret_key', WithDecryption=True),
        # MAIL_USERNAME = ssm.get_parameter(Name='mail_username', WithDecryption=True),
        # MAIL_PASSWORD = ssm.get_parameter(Name='mail_password', WithDecryption=True),
        # #CELERY_RESULT_BACKEND = ssm.get_parameter(Name='/mail_username', WithDecryption=True),
        # CELERY_BROKER_URL = ssm.get_parameter(Name='celery_broker_url', WithDecryption=True),
        # GIPHY_API_KEY = ssm.get_parameter(Name='giphy_api_key', WithDecryption=True),
    
    ))
    app.config.update(CELERY_RESULT_BACKEND=app.config['MONGO_CONNECTION_STRING'])
    app.config.update(SURVEY_INTERVAL_BASE=3600*24*30*3)
    app.config.update(SURVEY_INTERVAL_CHANGE=3600*24*14)
    app.config.update(NOTIFICATION_INTERVAL=3600*24*2)
    app.config.update(RUN_CALCULATE_GLOBAL_STATISTICS_PERIOD=3600*1)
    app.config.update(SAVE_COPY_USERS_EMOTION_PROFILE_PERIOD=3600*1)
app.config.update(RASA_HOSTNAME=os.environ['RASA_HOSTNAME'])
app.config.update(RASA_PORT=os.environ['RASA_PORT'])
from .data import dataclass
# mongodb mongoengine
connect(host=app.config["MONGO_CONNECTION_STRING"])
app.config.update(dict(
    DEBUG=True,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False
))
if not dataclass.GlobalStatistics.objects.first():
    stats=dataclass.GlobalStatistics()
    stats.save()
GIPHY_TAGS=['fun','movies','vacation','animals','holidays','cute','happy','pets','celebrities','nature']

mail = Mail()
mail.init_app(app)
totp = pyotp.TOTP(app.config["OTP_SECRET_KEY"])
from .models import goemotions

from . import giphyUtil
giphy_util = giphyUtil.GiphyUtil(app.config['GIPHY_API_KEY'])
from . import recommender
from . import rasa
rasa_client = rasa.Rasa_Client(host_name=app.config['RASA_HOSTNAME'],port=app.config['RASA_PORT'])
from .celery_config import celery_app
celery_app = celery_app
from . import server
app.register_blueprint(server.main_bp)

if IS_DEV:
    app.register_blueprint(server.internal_bp)

__all__ = ['rasa', 'dataclass', 'recommender','giphyUtil','goemotions']
