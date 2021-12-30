from .data.dialogue import Dialogue,Sentence
from .rasa import Rasa_Client
from flask import request, Response, Blueprint, current_app

import json
import jwt
from flask_mail import Mail, Message as FlaskMessage

from hashlib import sha256
from datetime import datetime, timedelta
from mongoengine import *
from .dataclass import *
from random import randint, uniform
import uuid
from werkzeug.exceptions import HTTPException


# main flask app object for configer dependencies only
# endpoints are defined using blueprints, global flask app object is accessed by current_app
from backend import app,rasa_client,totp,mail,celery_app
main_bp = Blueprint('main', __name__)
internal_bp = Blueprint('internal', __name__)

AUTH_TOKEN_HEADER_NAME = 'rasa-access-token'
CHAT_SESSION_IDENTIFIER_NAME = 'chat-session-uuid'


def _hash_password(pw):
    return sha256(pw.encode('utf-8')).hexdigest()


def _encode_jwt(obj):
    return jwt.encode(obj, current_app.config['SECRET_KEY'], algorithm="HS256")


def _decode_jwt(token):
    return jwt.decode(
        token, current_app.config['SECRET_KEY'], algorithms=["HS256"])


@main_bp.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
        "message": 'An error occured'
    })
    response.content_type = "application/json"
    return response


def token_required(f):

    def wrapper(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if AUTH_TOKEN_HEADER_NAME in request.headers:
            token = request.headers[AUTH_TOKEN_HEADER_NAME]
        # return 401 if token is not passed
        if not token:
            return json.dumps({'message': 'Token is missing !!'}), 401

            # decoding the payload to fetch the stored details
        data = _decode_jwt(
            token)
        current_user = User.objects(username=data['username'])\
            .first()

        if current_user is None:
            return json.dumps({
                'message': 'Token is invalid !!'
            }), 401
        # returns the current logged in users contex to the routes
        return f(current_user, data, *args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper
# route for logging user in


@main_bp.route('/login', methods=['POST'])
def login():
    # creates dictionary of form data
    auth = request.form

    if not auth or not auth.get('password'):
        # returns 401 if any email or / and password is missing
        return Response(
            json.dumps({"message": 'Could not verify'}),
            401,
            mimetype='application/json'
        )

    user = User.objects(username=auth.get('username'))\
        .first()

    # no such user
    if user is None:
        return Response(
            json.dumps({"message": 'Could not verify'}),
            401,
            mimetype='application/json'
        )
    if not user.is_email_verified:
        return Response(
            json.dumps({"message": 'Account not email verified'}),
            401,
            mimetype='application/json'
        )
    # generates auth token
    # logger.info(user.password)
    # logger.info(hash(auth.get('password')))
    if user.password == _hash_password(auth.get('password')):
        # generates the JWT Token
        token = _encode_jwt({
            'username': user.username,
            'exp': datetime.utcnow() + timedelta(minutes=30),
            CHAT_SESSION_IDENTIFIER_NAME: str(uuid.uuid4())
        })

        return Response(json.dumps({AUTH_TOKEN_HEADER_NAME: token}), 200, mimetype='application/json')
    # wrong password
    return Response(
        json.dumps({"message": 'Could not verify'}),
        403,
        mimetype='application/json'
    )

@celery_app.task
def _sendVerificationEmail(address, otp):
    with app.app_context():
        msg = FlaskMessage(
            f"Verification code for registration: {otp}", sender=app.config["EMAIL_VERIFICATION_SENDER_ADDRESS"], recipients=[address])
        mail.send(msg)

@main_bp.route('/signup', methods=['POST'])
def signup():
    _sendVerificationEmail.delay("ccysimon476@gmail.com","celery")
    # creates a dictionary of the form data
    data = request.form

    # gets name, email and password
    username, email = data.get('username'), data.get('email')
    password = data.get('password')

    # checking for existing user
    user = User.objects(username=username).count()
    if not user:
        # database ORM object
        otp = totp.now()
        user = User(
            username=username,
            email=email,
            password=_hash_password(password),
            otp=_hash_password(otp)
        )

        _sendVerificationEmail.delay(email, otp)
        # insert user
        user.save()

        return Response(json.dumps({"message": 'Successfully registered. Please verify your email.'}), 201, mimetype='application/json')
    else:
        # returns 202 if user already exists
        return Response(json.dumps({"message": 'User already exists. Please Log in.'}), 202, mimetype='application/json')


# {   
#     'otp': 123456,
#     'email': test@gmail.com
# }
@main_bp.route("/signup/verification", methods=['POST'])
def otpVerification():
    data = request.form
    user = User.objects(email=data.get('email')).first()
    otp = data.get('otp')
    if not user:
        return Response(json.dumps({"message": "user not found"}), status=404, mimetype='application/json')
    if not otp:
        return Response(json.dumps({"message": "missing otp"}), status=404, mimetype='application/json')

    if user.otp == _hash_password(otp):
        user.is_email_verified = True
        user.save()
        return Response(json.dumps({"message": "Successfully verifed"}), status=200, mimetype='application/json')
    else:
        return Response(json.dumps({"message": "Wrong otp"}), status=404, mimetype='application/json')


@main_bp.route("/signup/resend-verification-email", methods=['POST'])
def resendEmail():
    data = request.form
    user = User.objects(email=data.get('email')).first()
    if not user:
        return Response(json.dumps({"message": "user not found"}), status=404, mimetype='application/json')
    try:
        otp = totp.now()
        user.otp = _hash_password(otp)
        _sendVerificationEmail.delay(user.email, otp)
        user.save()
        return Response(json.dumps({"message": "Email resent"}), status=200, mimetype='application/json')
    except:
        return Response(json.dumps({"message": "An error occured"}), status=404, mimetype='application/json')


@main_bp.route("/", methods=['GET'])
def connection_ok():
    return Response(json.dumps({"message": "hi"}), status=200, mimetype='application/json')

# Request:
# {
#   "message": "Hi"
# }
# Response:
# [
#     {
#         "recipient_id": "test_user",
#         "text": "Hey! How are you?"
#     }
# ]


@main_bp.route("/", methods=['POST'])
@token_required
def send_message(user, token_body):
    content = request.form
    # print(content['message'])
    json_string, status = rasa_client.send_message(
        content.get('message'), token_body[CHAT_SESSION_IDENTIFIER_NAME])
    return Response(json_string, status=status, mimetype='application/json')


# Request:
# {
#   "sentences": [{"speaker": "user", "text": "hi","intent":"greet"},{"speaker": "bot", "text": "hi"}]
# }
@main_bp.route("/add_data", methods=['POST'])
def add_training_data():
    content = request.json
    dialogue = Dialogue(**content)
    rasa_client.add_training_data(dialogue)
    return Response()

# Request:
# {
#   "media_name": "bird1",
#   "score": 0.5
# }


@main_bp.route("/add_preference", methods=['POST'])
@token_required
def add_preference_to_user(current_user, token_body):
    data = request.json
    media_name = data.get('media_name')
    score = data.get('score')
    media = MultiMediaData.objects(name=media_name).first()
    if media is None:
        return Response(
            json.dumps({"message": 'Media not found'}),
            404,
            mimetype='application/json'
        )
    current_user.preferences.append(Preference(media, score))
    return Response('', 204)


@main_bp.route("/new-chat-session", methods=['POST'])
@token_required
def new_chat_session(user, token_body):
    new_token = _encode_jwt(
        dict(token_body, **{CHAT_SESSION_IDENTIFIER_NAME: str(uuid.uuid4())}))
    return Response(json.dumps({AUTH_TOKEN_HEADER_NAME: new_token}), status=200, mimetype='application/json')


@internal_bp.route("/train", methods=['POST'])
def train_data():
    return rasa_client.train()

# bad method?


@internal_bp.route("/arbitrary_code", methods=['POST'])
def _do_stuff():
    for x in range(10):
        user = User(username=f"{x}")
        multimedia = MultiMediaData(name=f"{x}")
        user.save()
        multimedia.save()
    # contentx = MultiMediaData(name="x")
    # contentx.save()
    # userx = User(username= "x",preferences=[Preference(content=contentx,score=1.0)])
    # userx.save()
    for user in User.objects():
        user.preferences = []
        for x in range(10):
            if randint(0, 2) == 0:
                pref = Preference(content=MultiMediaData.objects(
                    name=f"{x}").first(), score=uniform(0, 1))
                user.preferences.append(pref)
        user.save()

    # multimedia.save()
    return Response()
