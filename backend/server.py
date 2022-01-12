from .data.dialogue import Dialogue
from flask import request, Response, Blueprint, current_app

import json
import jwt
from flask_mail import Message as FlaskMessage

from hashlib import sha256
from datetime import datetime, timedelta
from mongoengine import *
from .dataclass import *
from random import randint, uniform
import uuid

# main flask app object for configer dependencies only
# endpoints are defined using blueprints, global flask app object is accessed by current_app
from backend import app,rasa_client,totp,mail,celery_app
main_bp = Blueprint('main', __name__)
internal_bp = Blueprint('internal', __name__)

AUTH_TOKEN_HEADER_NAME = 'rasa-access-token'


def _hash_password(pw):
    return sha256(pw.encode('utf-8')).hexdigest()

def _get_jwt_encode_key(extra = None):
    if extra:
        m = sha256()
        m.update(current_app.config['SECRET_KEY'].encode('utf-8'))
        m.update(extra.encode('utf-8'))
        return m.hexdigest() 
    else:
        return current_app.config['SECRET_KEY']

def _encode_jwt(obj, second_par = None):
    return jwt.encode(obj, _get_jwt_encode_key(second_par), algorithm="HS256")


def _decode_jwt_without_verifying(token):
    return jwt.decode(
        token, _get_jwt_encode_key(), algorithms=["HS256"], options={"verify_signature": False})

def _verify_jwt(token, second_par):
    return jwt.decode(
        token, _get_jwt_encode_key(second_par), algorithms=["HS256"])
def _create_new_conversation(user):
    new_uuid = str(uuid.uuid4())
    user.latest_conversation_uuid = new_uuid
    new_conversation = Conversation(uuid=new_uuid, user=user)
    new_conversation.save()
    new_conversation_with_id = Conversation.objects(uuid=new_uuid).first()
    user.conversations.append(new_conversation_with_id)
    user.save()
    return user,new_conversation_with_id
@main_bp.errorhandler(Exception)
def handle_exception(e):
    current_app.logger.exception('An error occured')
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = Response(status=500)
    # replace the body with JSON
    response.data = json.dumps({
        "code": 500,
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
            return Response(json.dumps({'message': 'Token is missing !!'}), 401, mimetype='application/json')

        try:
            # decoding the payload to fetch the stored details
            data = _decode_jwt_without_verifying(
                token)
        except jwt.exceptions.ExpiredSignatureError:
            return Response(json.dumps({'message': 'Token has expired'}),401, mimetype='application/json')
        current_user = User.objects(username=data['username'])\
            .first()
            
        if current_user is None:
            return Response(json.dumps({
                'message': 'Token is invalid !!'
            }), 401, mimetype='application/json')
        try:
            _verify_jwt(token,current_user.password)
        except jwt.exceptions.InvalidSignatureError:
            return Response(json.dumps({'message': 'Invalid token'}),401, mimetype='application/json')
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
            'exp': datetime.utcnow() + timedelta(days=30)
        },user.password)

        return Response(json.dumps({AUTH_TOKEN_HEADER_NAME: token}), 200, mimetype='application/json')
    # wrong password
    return Response(
        json.dumps({"message": 'Could not verify'}),
        403,
        mimetype='application/json'
    )

@celery_app.task
def _sendVerificationEmail(address, text_body):
    with app.app_context():
        msg = FlaskMessage(text_body, sender=app.config["EMAIL_VERIFICATION_SENDER_ADDRESS"], recipients=[address])
        mail.send(msg)

@main_bp.route('/signup', methods=['POST'])
def signup():
        # creates a dictionary of the form data
        data = request.form

        # gets name, email and password
        username, email = data.get('username'), data.get('email')
        password = data.get('password')

        # checking for existing user
        is_user_exist = User.objects(username=username).count()
        is_email_exist = User.objects(email=email).count()
        if not is_user_exist and not is_email_exist:
            # database ORM object
            otp = totp.now()
            user = User(
                username=username,
                email=email,
                password=_hash_password(password),
                otp=_hash_password(otp)
            )

            _sendVerificationEmail.delay(email, f"Verification code for registration: {otp}")
            user.save()
            _create_new_conversation(user)
            
            return Response(json.dumps({"message": 'Successfully registered. Please verify your email.'}), 201, mimetype='application/json')
        else:
            # returns 202 if user already exists
            return Response(json.dumps({"message": 'Username or email already exists. Please Log in.'}), 202, mimetype='application/json')


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
        _sendVerificationEmail.delay(user.email, f"Verification code for registration: {otp}")
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
    user_message= content.get('message')
    json_string, status = rasa_client.send_message(
        str(user_message), user.latest_conversation_uuid)
    current_conversation =  Conversation.objects(uuid=user.latest_conversation_uuid).first()
    bot_reply = json.loads(json_string)[0]['text']
    user_message_obj = Message(content=user_message,is_from_user=True,time_sent=datetime.utcnow())
    bot_message_obj = Message(content=bot_reply,is_from_user=False,time_sent=datetime.utcnow())
    current_conversation.content.append(user_message_obj)
    current_conversation.content.append(bot_message_obj)
    current_conversation.save()

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
    return Response(json.dumps({'message': 'Prefence added'}), status=200, mimetype='application/json')


@main_bp.route("/new-chat-session", methods=['POST'])
@token_required
def new_chat_session(user, token_body):
    if user.conversations.__len__()==0:
        _create_new_conversation(user)
        current_app.logger.warn(f"User: {user.username} does not have an existing conversation, creating a new one")
        return Response(json.dumps({'message': 'New chat session created'}), status=200, mimetype='application/json')
    if user.conversations[0].content.__len__() ==0:
        current_app.logger.info(f"User: {user.username} attempted to start a new conversation without finishing the last one")
        return Response(json.dumps({'message': 'New chat session created'}), status=200, mimetype='application/json')
    _create_new_conversation(user)
    return Response(json.dumps({'message': 'New chat session created'}), status=200, mimetype='application/json')

@main_bp.route("/delete-profile", methods=['DELETE'])
@token_required
def delete_user(user, token_body):
    user.delete()
    return Response(json.dumps({'message': 'Profile deleted'}), status=200, mimetype='application/json')

class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        return json.JSONEncoder.default(self, o) 

@main_bp.route("/show-profile", methods=['GET'])
@token_required
def get_user_profile(user, token_body):
    user.password = None
    user.otp = None
    user_json = json.loads(user.to_json())
    new_list = []
    for entry in user.conversations:
        new_list.append(json.loads(entry.to_json()))
    user_json["conversations"]=new_list
    return Response(json.dumps(user_json,cls=DateTimeEncoder),200, mimetype='application/json')

@main_bp.route("/signup/forget-password", methods=['POST'])
def reset_pw_sendEmail():
    data = request.form
    user = User.objects(email=data.get('email')).first()
    if not user:
        return Response(json.dumps({"message": "user not found"}), status=404, mimetype='application/json')
    try:
        otp = totp.now()
        user.otp = _hash_password(otp)
        _sendVerificationEmail.delay(user.email, f"Code for resetting password: {otp}")
        user.save()
        return Response(json.dumps({"message": "Email sent"}), status=200, mimetype='application/json')
    except:
        return Response(json.dumps({"message": "An error occured"}), status=404, mimetype='application/json')

@main_bp.route("/signup/reset-password", methods=['POST'])
def reset_pw():
    data = request.form
    email = data.get('email')
    otp = data.get('otp')
    new_password = data.get('password')
    if not otp:
        return Response(json.dumps({"message": "missing otp"}), status=404, mimetype='application/json')
    user = User.objects(email=email).first()
    if not user:
        return Response(json.dumps({"message": "user not found"}), status=404, mimetype='application/json')
    
    if _hash_password(otp) == user.otp:
        user.is_verified=True
        user.password=_hash_password(new_password)
        user.save()
        return Response(json.dumps({"message":"Resetted password"}), status=200, mimetype='application/json')
    else:
        return Response(json.dumps({"message": "Wrong otp"}), status=404, mimetype='application/json')
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
