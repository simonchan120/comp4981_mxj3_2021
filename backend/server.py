import logging
import string
from unicodedata import name

from flask import request, Response, Blueprint, current_app

import json
import jwt
from flask_mail import Message as FlaskMessage

from hashlib import sha256
from mongoengine import *
from .data.dialogue import Dialogue
from .data.dataclass import Survey,Message,MultiMediaData,Preference,User,Conversation, EmotionProfile, EmotionProfileList, MessageTypes, GlobalStatistics, Statistic
from random import randint, random, uniform, choices
import uuid
from datetime import datetime,timezone,timedelta
# main flask app object for configer dependencies only
# endpoints are defined using blueprints, global flask app object is accessed by current_app
from backend import app,rasa_client,totp,mail,celery_app, recommender, giphyUtil
main_bp = Blueprint('main', __name__)
internal_bp = Blueprint('internal', __name__)
AUTH_TOKEN_HEADER_NAME = 'rasa-access-token'

DEFAULT_DATE_DISPLAY_FORMAT="%d-%b-%Y (%H:%M:%S)"
DEFAULT_UTC = timezone(timedelta(hours=8))
logger = logging.getLogger(__name__)
User._survey_period = app.config['SURVEY_INTERVAL_BASE']
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
@main_bp.errorhandler(Exception)
def handle_exception(e):
    current_app.logger.exception('An error occured')
    """Return JSON instead of HTML for HTTP errors."""
    return Response(json.dumps({'message':"An error occured"}), 500, mimetype='application/json')


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
        except Exception:
            return Response(json.dumps({'message':'Error processing jwt token'}),400, mimetype='application/json')
        user = User.objects(username=data['username'])\
            .first()
        
        if user is None:
            return Response(json.dumps({
                'message': 'Token is invalid !!'
            }), 401, mimetype='application/json')
        try:
            _verify_jwt(token,user.password)
        except jwt.exceptions.InvalidSignatureError:
            return Response(json.dumps({'message': 'Invalid token'}),401, mimetype='application/json')
        except jwt.exceptions.ExpiredSignatureError:
            return Response(json.dumps({'message': 'Please re-login'}),401, mimetype='application/json')
        # returns the current logged in users contex to the routes
        return f(user, data, *args, **kwargs)
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
    if user.password  == _hash_password(auth.get('password')+user.salt if user.salt else ''):
        # generates the JWT Token
        token = _encode_jwt({
            'username': user.username,
            'exp': datetime.utcnow() + timedelta(days=30)
        },user.password)

        return Response(json.dumps({AUTH_TOKEN_HEADER_NAME: token}), 200, mimetype='application/json')
    # wrong password
    return Response(
        json.dumps({"message": 'Could not verify'}),
        401,
        mimetype='application/json'
    )

@celery_app.task
def _sendVerificationEmail(address, text_body):
    with app.app_context():
        msg = FlaskMessage(text_body, sender=app.config["MAIL_USERNAME"], recipients=[address])
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
            salt = ''.join(choices(string.ascii_letters + string.digits, k=16))
            user = User(
                username=username,
                email=email,
                password=_hash_password(password+salt),
                otp=_hash_password(otp),
                salt = salt
            )
            _sendVerificationEmail.delay(email, f"Verification code for registration: {otp}")
            user.init_new_user()
            logger.debug(f"Creating user: {user.username}, conversation_list len: {len(user.conversations)}")
            
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
    response_obj, status = rasa_client.send_message(user,
        str(user_message))
    current_conversation =  user.latest_conversation
    bot_reply = response_obj[0]['text']
    response_obj[0]['type']='text'

    user_message_obj = Message(content=user_message,is_from_user=True,type=MessageTypes.TEXT)
    bot_message_obj = Message(content=bot_reply,is_from_user=False,type=MessageTypes.TEXT)
    
    current_conversation.content.append(user_message_obj)
    current_conversation.content.append(bot_message_obj)

    recommender.Recommender.process_message(user,user_message,current_conversation,response_obj)

    current_conversation.save()

    return Response(json.dumps(response_obj), status=status, mimetype='application/json')


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


@main_bp.route("/add-preference", methods=['POST'])
@token_required
def add_preference_to_user(user, token_body):
    data = request.form
    media_name = data.get('name')
    score = data.get('score')
    if media_name is None or score is None:
        return Response(json.dumps({"message":"Missing fields"}),404,
            mimetype='application/json')
    try:
        float(score)
    except ValueError:
        return Response(json.dumps({"message":"invalid score"}),404,
            mimetype='application/json')
    media = MultiMediaData.objects(name=media_name).first()
    if media is None:
        return Response(
            json.dumps({"message": 'Media not found / Wrong name'}),
            404,
            mimetype='application/json'
        )
    existing_preference = next((x for x in user.preferences if x.content.name == media_name),None)
    if existing_preference:
        existing_preference.score = float(score)
    else:
        user.preferences.append(Preference(content=media, score=score))
    user.save()
    return Response(json.dumps({'message': 'Prefence added'}), status=200, mimetype='application/json')


@main_bp.route("/new-chat-session", methods=['POST'])
@token_required
def new_chat_session(user: User, token_body):
    current_app.logger.debug(f'len of conversations: {len(user.conversations)} for user: {user.username}')
    if user.conversations.__len__()==0:
        user.create_new_conversation()
        current_app.logger.warn(f"User: {user.username} does not have an existing conversation, creating a new one")
        return Response(json.dumps({'message': 'New chat session created'}), status=200, mimetype='application/json')
    if user.conversations[0].content.__len__() ==0:
        current_app.logger.info(f"User: {user.username} attempted to start a new conversation without finishing the last one")
        return Response(json.dumps({'message': 'New chat session created'}), status=200, mimetype='application/json')
    user.create_new_conversation()
    return Response(json.dumps({'message': 'New chat session created'}), status=200, mimetype='application/json')

@main_bp.route("/delete-profile", methods=['DELETE'])
@token_required
def delete_user(user, token_body):
    user.delete()
    return Response(json.dumps({'message': 'Profile deleted'}), status=200, mimetype='application/json')

def _preprocess_user_profile(d,user_utc):
    if isinstance(d, dict):
        for key in list(d.keys()):

            if '$' in key and len(key) > 1:
                new_key_name =  key.replace('$','')
                d[new_key_name]=d[key]
                del d[key]
                key = new_key_name
            
            if key=='date':
                new_date = datetime.fromtimestamp(d[key]/1000) +timedelta(hours=user_utc)
                d[key] = new_date.strftime(DEFAULT_DATE_DISPLAY_FORMAT)
            elif key == '_id' or key == 'oid' or 'uuid' in key:
                del d[key]
                continue
            _preprocess_user_profile(d[key],user_utc)
    if isinstance(d, list):
        for item in d:
            _preprocess_user_profile(item,user_utc)

@main_bp.route("/show-profile", methods=['GET'])
@token_required
def get_user_profile(user: User, token_body):
    is_verbose = False

    data = request.form
    try:
        is_verbose = data.get('verbose').lower() == 'true'
    except (ValueError, AttributeError):
        pass
    user.password = None
    user.otp = None
    user_json = json.loads(user.to_json())
    user_json['conversations']= [json.loads(x.to_json()) for x in user.conversations]
    user_json['preferences'] = [({'content':json.loads(x.content.to_json()),'score':x.score}) for x in user.preferences]
    user_json['pred_preferences'] = [({'content':json.loads(x.content.to_json()),'score':x.score}) for x in user.pred_preferences]
    user_json['latest_conversation'] = json.loads(user.latest_conversation.to_json())
    if not is_verbose:
        #user_timezone = timezone(timedelta(hours=user.utc_in_hours))
        _preprocess_user_profile(user_json,user.utc_in_hours)
    return Response(json.dumps(user_json),200, mimetype='application/json')

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
        user.salt=''.join(choices(string.ascii_letters + string.digits, k=16))
        user.password=_hash_password(new_password+user.salt if user.salt else '')
        user.save()
        return Response(json.dumps({"message":"Resetted password"}), status=200, mimetype='application/json')
    else:
        return Response(json.dumps({"message": "Wrong otp"}), status=404, mimetype='application/json')
    
@main_bp.route("/add-survey-results",methods=['POST'])
@token_required
def add_survey_results(user: User,token_body):
    data=request.form
    d1,d2,d3,d4,d5,d6,d7,d8,d9=data.get('field_1'),data.get('field_2'),data.get('field_3'),data.get('field_4'),data.get('field_5'),data.get('field_6'),data.get('field_7'),data.get('field_8'),data.get('field_9')
    if not d1 or not d2 or not d3 or not d4 or not d5 or not d6 or not d7 or not d8 or not d9:
        return Response(json.dumps({"message": "missing survey fields"}),status=404,mimetype='application/json')
    try:
        [d1,d2,d3,d4,d5,d6,d7,d8,d9] = [int(x) for x in [d1,d2,d3,d4,d5,d6,d7,d8,d9]]
    except ValueError:
    #if not d1.isnumeric() or not d2.isnumeric() or not d3.isnumeric() or not d4.isnumeric() or not d5.isnumeric() or not d6.isnumeric() or not d7.isnumeric()or not d8.isnumeric()or not d9.isnumeric():
        return Response(json.dumps({"message": "invalid survey values, expected integers"}),status=404, mimetype='application/json')
    #survey = Survey(survey_entry_1=d1,survey_entry_2=d2,survey_entry_3=d3,survey_entry_4=d4,survey_entry_5=d5,survey_entry_6=d6,survey_entry_7=d7,survey_entry_8=d8,survey_entry_9=d9)
    
    survey = Survey.create_survey(d1,d2,d3,d4,d5,d6,d7,d8,d9)
    if not survey:
        return Response(json.dumps({f"message": "invalid survey values"}),status=404, mimetype='application/json')
    user.add_new_survey(survey)
    user.save()

    return Response(json.dumps({"message": "Survey result saved", "result": survey.result}),status=200,mimetype='application/json')

@main_bp.route("/check-do-survey",methods=['GET'])
@token_required
def check_do_survey(user:User,token_body):
    
    latest_survey_time = user.surveys[0].time_submitted  if len(list(user.surveys)) >= 1 else datetime(year = 1971,month=1,day=1)
    seconds_since_last_survey = (datetime.utcnow()-latest_survey_time).total_seconds()
    base_interval = current_app.config['SURVEY_INTERVAL_BASE']
    change_interval = current_app.config['SURVEY_INTERVAL_CHANGE']
    threshold = base_interval

    MAX_SUM_OF_EMOTION_SCORE_DIFFERENCE = 100
    
    result_change = False
    if user.previous_emotion_profile_lists and user.previous_emotion_profile_lists[0].profile_list:
        current_emotion_profile_list = user.previous_emotion_profile_lists[0].profile_list
        sum_of_emotion_score_difference = sum([abs(current_emotion_profile_list[i+1].chat_score-current_emotion_profile_list[i].chat_score) for i in range(0, len(current_emotion_profile_list)-1)])

        if sum_of_emotion_score_difference >= MAX_SUM_OF_EMOTION_SCORE_DIFFERENCE:
            result_change = seconds_since_last_survey >= change_interval

    result_base = seconds_since_last_survey >= threshold
    result = result_base or result_change
    return Response(json.dumps({"result": result, "last_survey":latest_survey_time.strftime(DEFAULT_DATE_DISPLAY_FORMAT)}),status=200,mimetype='application/json')

@main_bp.route("/check-send-push-notification",methods=['GET'])
@token_required
def check_send_push_notification(user: User,token_body):
    current_conversation=user.latest_conversation
    latest_message_time =  current_conversation.content[0].time_sent if len(list(current_conversation.content)) >= 1 else datetime(year = 1971,month=1,day=1)
    seconds_since_last_message = (datetime.utcnow()-latest_message_time).total_seconds()
    base_interval = current_app.config['NOTIFICATION_INTERVAL']
    threshold = base_interval
    result = seconds_since_last_message >= threshold
    return Response(json.dumps({"result": result, "last_message":latest_message_time.strftime(DEFAULT_DATE_DISPLAY_FORMAT)}),status=200,mimetype='application/json')

@main_bp.route("/get-global-statistics",methods=['GET'])
# @token_required
# def get_global_statistics(user, token_body):
def get_global_statistics():
    data = request.args
    start,end = data.get("start_time"), data.get("end_time")
    if start:
        try:
            start = datetime.fromtimestamp(int(start))
        except (ValueError, OverflowError, OSError):
            return Response(json.dumps({"message": 'Invalid value for start_time'}),status=404,mimetype='application/json')
    if end:
        try:
            end = datetime.fromtimestamp(int(end))
        except (ValueError, OverflowError, OSError):
            return Response(json.dumps({"message": 'Invalid value for end_time'}),status=404,mimetype='application/json')
    if not end: 
        end = datetime.utcnow()
    if start and end and start>end:
        return Response(json.dumps({"message": 'start_time has a large value then end_time'}),status=404,mimetype='application/json')
    global_statistics: GlobalStatistics = GlobalStatistics.objects.first()
    statistics = []
    if not start:
        recent_statistic=global_statistics.get_recent_statistic()
        statistics.append(recent_statistic)
    else:
        #start,end = datetime.fromtimestamp(int(start)), datetime.fromtimestamp(int(end))
        #query_statistics = list(global_statistics.statistics((Q(time_recorded__gte=start) & Q(time_recorded__lte=end))))
        query_statistics = list(filter(lambda x:start<= x.time_recorded and x.time_recorded <= end,
                               global_statistics.statistics))

        statistics.extend(query_statistics)
    if statistics is None:
        end = start
        start = start + timedelta(hours = -1)
        query_statistics = list(filter(lambda x:start<= x.time_recorded and x.time_recorded <= end,
                               global_statistics.statistics))

        statistics.extend(query_statistics)
    users_average_chat_score = sum(x.users_average_chat_score for x in statistics)/ len(statistics)
    users_average_full_score = sum(x.users_average_full_score for x in statistics)/ len(statistics)

    return Response(json.dumps({'users_average_chat_score':users_average_chat_score,
    'users_average_full_score':users_average_full_score}),status=200,mimetype='application/json')

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

@internal_bp.route("/add_giphy_tags",methods=['POST'])
def _add_giphy_tag():
    GIPHY_TAGS=['fun','movies','vacation','animals','holidays','cute','happy','pets','celebrities','nature']
    MultiMediaData.objects.insert([MultiMediaData(name=x,description='giphy_tag')for x in GIPHY_TAGS])
    return Response()