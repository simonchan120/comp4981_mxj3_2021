from flask import Flask, request,Response
from rasa import Rasa_Client
from data.dialogue import Sentence,Dialogue

rasa_client = Rasa_Client()
#rasa_client.send_message("Hello!")

app = Flask(__name__)


#Request:
# {
#   "message": "Hi"
# }
#Response:
# [
#     {
#         "recipient_id": "test_user",
#         "text": "Hey! How are you?"
#     }
# ]
@app.route("/", methods=['POST'])
def send_message():
    content = request.json
    #print(content['message'])
    json_string,status = rasa_client.send_message(content['message'])
    return Response(json_string, status=status, mimetype='application/json')


#Request:
# {
#   "sentences": [{"speaker": "user", "text": "hi","intent":"greet"},{"speaker": "bot", "text": "hi"}]
# }
@app.route("/add_data",methods=['POST'])
def add_training_data():
    content = request.json
    dialogue = Dialogue(**content)
    rasa_client.add_training_data(dialogue)
    return Response()

#Request:
# {
#   "
# }
@app.route("/train",methods=['POST'])
def train_data():
    return rasa_client.train()