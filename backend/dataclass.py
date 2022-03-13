from mongoengine import *
from mongoengine.fields import BooleanField, EmbeddedDocumentField, EmbeddedDocumentListField, IntField, ListField, ReferenceField, SortedListField
from datetime import datetime
class Survey(EmbeddedDocument):
    time_submitted = DateTimeField(default=datetime.utcnow)
    name = StringField(default="PMH-Scale")
    survey_entry_1 = IntField()
    survey_entry_2 = IntField()
    survey_entry_3 = IntField()
    survey_entry_4 = IntField()
    survey_entry_5 = IntField()
    survey_entry_6 = IntField()
    survey_entry_7 = IntField()

class Message(EmbeddedDocument):
    content = StringField()
    is_from_user = BooleanField()
    time_sent = DateTimeField(default=datetime.utcnow)

#https://github.com/MongoEngine/mongoengine/issues/1697
class MultiMediaData(Document):
    name = StringField(unique=True)
    description = StringField()
    content = BinaryField()

class Preference(EmbeddedDocument):
    content = ReferenceField(MultiMediaData)
    score = FloatField()

class User(Document):
    email = StringField()
    username = StringField(max_length=50,unique=True,required=True)
    password = StringField()
    is_email_verified = BooleanField(default=False)
    otp = StringField()
    conversations = ListField(ReferenceField('Conversation'))
    time_registered = DateTimeField(default=datetime.utcnow)
    gender = StringField()
    age = IntField()
    year_of_school_or_work = IntField()
    is_student = BooleanField()
    is_ust = BooleanField()
    emotion_score = FloatField(default=0.5)
    surveys = SortedListField(EmbeddedDocumentField('Survey',ordering="time_submitted",reverse = True))
    preferences = SortedListField(EmbeddedDocumentField('Preference'),ordering="score",reverse = True)
    pred_preferences = SortedListField(EmbeddedDocumentField('Preference'),ordering="score",reverse = True)
    latest_conversation_uuid = StringField()

class Conversation(Document):
    time_started = DateTimeField(default=datetime.utcnow, required=True)
    time_ended = DateTimeField()
    uuid = StringField()
    user = ReferenceField('User',reverse_delete_rule=CASCADE)
    content = SortedListField(EmbeddedDocumentField('Message'),ordering="time_sent",reverse = True)






