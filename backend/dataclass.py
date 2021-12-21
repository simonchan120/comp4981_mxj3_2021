from mongoengine import *
from mongoengine.fields import EmbeddedDocumentField, EmbeddedDocumentListField, ListField, ReferenceField, SortedListField

class Survey(EmbeddedDocument):
    time_submitted = DateTimeField()
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
    is_from_user = BinaryField()
    time_sent = DateTimeField()

#https://github.com/MongoEngine/mongoengine/issues/1697
class MultiMediaData(Document):
    name = StringField()
    description = StringField()
    content = BinaryField()

class Preference(EmbeddedDocument):
    content = ReferenceField(MultiMediaData)
    score = FloatField()

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
    surveys = EmbeddedDocumentListField('Survey')
    preferences = SortedListField(EmbeddedDocumentField('Preference'),ordering="score",reverse = True)
    pred_preferences = SortedListField(EmbeddedDocumentField('Preference'),ordering="score",reverse = True)

class Conversation(Document):
    time_started = DateTimeField()
    time_ended = DateTimeField()
    user = ReferenceField('User',reverse_delete_rule=CASCADE)
    content = EmbeddedDocumentListField('Message')






