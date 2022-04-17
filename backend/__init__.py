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
LOGGING_FOLDER = "backend/logs"
Path(f"{LOGGING_FOLDER}").mkdir(parents=True, exist_ok=True)
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
            'level': 'INFO',
            'formatter': 'default',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',  # Default is stderr
    }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['default']
    }
})
app = Flask(__name__)

if os.environ['FLASK_ENV']=='development':
# TODO: change this secret key before deployment
    app.config.from_file("config.json", load=json.load)

    app.config.update(SURVEY_INTERVAL_BASE=60)
    app.config.update(SURVEY_INTERVAL_CHANGE=60)
    app.config.update(NOTIFICATION_INTERVAL=60)

elif os.environ['FLASK_ENV']=='production':
    my_config = Config(
        region_name = 'ap-east-1',
        signature_version = 's3v4',
        retries = {
            'max_attempts': 10,
            'mode': 'standard'
        }
    )
    ssm = boto3.client('ssm',config=my_config)
    parameter = ssm.get_parameter(Name='/path/to/param', WithDecryption=True)
    app.config.update(a='a',b='b')

    app.config.update(SURVEY_INTERVAL_BASE=3600*24*30*3)
    app.config.update(SURVEY_INTERVAL_CHANGE=3600*24*14)
    app.config.update(NOTIFICATION_INTERVAL=3600*24*2)

# mongodb mongoengine
connect(host=app.config["MONGO_CONNECTION_STRING"])
app.config.update(dict(
    DEBUG=True,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,
    MAIL_USERNAME=app.config["EMAIL_VERIFICATION_SENDER_ADDRESS"],
    MAIL_PASSWORD=app.config["EMAIL_PASSWORD"],
))
mail = Mail()
mail.init_app(app)
totp = pyotp.TOTP(app.config["OTP_SECRET_KEY"])
from .data import dataclass
from . import recommender
from . import giphyUtil
from . import rasa
rasa_client = rasa.Rasa_Client()
from .celery_config import celery_app
celery_app = celery_app
from . import server
app.register_blueprint(server.main_bp)

if os.environ['FLASK_ENV']=='development':
    app.register_blueprint(server.internal_bp)

__all__ = ['rasa', 'dataclass', 'recommender','giphyUtil']
