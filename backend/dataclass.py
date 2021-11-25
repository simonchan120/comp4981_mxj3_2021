from mongoengine import *


class Message(EmbeddedDocument):
    content = StringField()
    is_from_user = BinaryField()
    time_sent = DateTimeField()

#https://github.com/MongoEngine/mongoengine/issues/1697



class User(Document):
    email = StringField()
    username = StringField(max_length=50,unique=True,required=True)
    password = StringField()
    #conversations = ListField(ReferenceField('Conversation'))
    time_registered = DateTimeField()
    gender = StringField()
    age = IntField()
    year_of_school_or_work = IntField()
    is_student = BinaryField()
    is_ust = BinaryField()

class Conversation(Document):
    time_started = DateTimeField()
    time_ended = DateTimeField()
    user = ReferenceField('User',reverse_delete_rule=CASCADE)
    content = ListField(EmbeddedDocumentField('Message'))

class Survey(Document):
    time_submitted = DateTimeField()
    user = ReferenceField('User')
    name = StringField(default="PMH-Scale")
    survey_entry_1 = IntField()