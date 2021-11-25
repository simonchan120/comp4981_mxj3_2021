from flask import Flask, request, Response
from rasa import Rasa_Client
from data.dialogue import Sentence, Dialogue
import logging
import json
import jwt
from hashlib import sha256
from datetime import datetime, timedelta
from dataclass import *
rasa_client = Rasa_Client()
# rasa_client.send_message("Hello!","admin")

app = Flask(__name__)
# TODO: change this secret key before deployment
app.config.from_file("config.json", load=json.load)
auth_token_header_name = 'rasa-access-token'

logger = logging.getLogger(__name__)
def token_required(f):
    
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if auth_token_header_name in request.headers:
            token = request.headers[auth_token_header_name]
        # return 401 if token is not passed
        if not token:
            return json.dumps({'message': 'Token is missing !!'}), 401

        
            # decoding the payload to fetch the stored details
        data = jwt.decode(token, app.config['SECRET_KEY'],algorithms=["HS256"])
        current_user = User.objects(username=data['username'])\
            .first()
        
        if current_user is None:
            return json.dumps({
                'message': 'Token is invalid !!'
            }), 401
        # returns the current logged in users contex to the routes
        return f(current_user, *args, **kwargs)

    return decorated
# route for logging user in


@app.route('/login', methods=['POST'])
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

    # generates auth token
    #logger.info(user.password)
    #logger.info(hash(auth.get('password')))
    if user.password == sha256(auth.get('password').encode('utf-8')).hexdigest():
        # generates the JWT Token
        token = jwt.encode({
            'username': user.username,
            'exp': datetime.utcnow() + timedelta(minutes=30)
        }, app.config['SECRET_KEY'],algorithm="HS256")

        return Response(json.dumps({auth_token_header_name: token}), 201)
    # wrong password
    return Response(
        json.dumps({"message": 'Could not verify'}),
        403,
        mimetype='application/json'
    )


@app.route('/signup', methods=['POST'])
def signup():
    # creates a dictionary of the form data
    data = request.form

    # gets name, email and password
    username, email = data.get('username'), data.get('email')
    password = data.get('password')

    # checking for existing user
    user = User.objects(username=username).count()
    if not user:
        # database ORM object
        user = User(
            username=username,
            email=email,
            password=sha256(password.encode('utf-8')).hexdigest()
        )
        # insert user
        user.save()

        return Response(json.dumps({"message": 'Successfully registered.'}), 201, mimetype='application/json')
    else:
        # returns 202 if user already exists
        return Response(json.dumps({"message": 'User already exists. Please Log in.'}), 202, mimetype='application/json')



@app.route("/", methods=['GET'])
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


@app.route("/", methods=['POST'])
@token_required
def send_message(user):
    content = request.json
    # print(content['message'])
    json_string, status = rasa_client.send_message(content['message'],user.username)
    return Response(json_string, status=status, mimetype='application/json')


# Request:
# {
#   "sentences": [{"speaker": "user", "text": "hi","intent":"greet"},{"speaker": "bot", "text": "hi"}]
# }
@app.route("/add_data", methods=['POST'])
def add_training_data():
    content = request.json
    dialogue = Dialogue(**content)
    rasa_client.add_training_data(dialogue)
    return Response()

# Request:
# {
#   "
# }


@app.route("/train", methods=['POST'])
def train_data():
    return rasa_client.train()
