
from flask_mail import Mail
from logging.config import dictConfig
from pathlib import Path
from flask import Flask
from datetime import datetime
import json
from mongoengine import connect
import pyotp
LOGGING_FOLDER="backend/logs"
Path(f"{LOGGING_FOLDER}").mkdir(parents=True, exist_ok=True)
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(module)s %(filename)s %(levelname)-8s %(message)s',
    }},
    'handlers': {'file': {
        'class': 'logging.handlers.RotatingFileHandler',
        'filename': f"{datetime.now().strftime(f'{LOGGING_FOLDER}/%Y%m%d-%H%M%S')}.log",
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['file']
    }
})
app = Flask(__name__)
# TODO: change this secret key before deployment
app.config.from_file("config.json", load=json.load)



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
from . import rasa
rasa_client = rasa.Rasa_Client()

from .celery_config import celery_app
celery_app = celery_app
from . import server
app.register_blueprint(server.main_bp)
app.register_blueprint(server.internal_bp)

__all__= ['rasa','server','dataclass','recommender']