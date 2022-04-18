from mongoengine import *
from mongoengine.fields import BooleanField, EmbeddedDocumentField, EnumField, IntField, ListField, ReferenceField, SortedListField
from datetime import datetime

from enum import Enum
import statistics
from typing import List
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
    survey_entry_8 = IntField()
    survey_entry_9 = IntField()
    result = FloatField()
    def calculate_survey_result(self):
        return round(sum((x-1)/3 for x in [self.survey_entry_1,self.survey_entry_2,self.survey_entry_3,self.survey_entry_4,self.survey_entry_5,self.survey_entry_6,self.survey_entry_7,self.survey_entry_8,self.survey_entry_9])/9,4)
    @staticmethod
    def create_survey(e1,e2,e3,e4,e5,e6,e7,e8,e9,name = None):
        survey = Survey(survey_entry_1=e1,survey_entry_2=e2,survey_entry_3=e3,survey_entry_4=e4,survey_entry_5=e5,survey_entry_6=e6,survey_entry_7=e7,survey_entry_8=e8,survey_entry_9=e9)
        if name:
            survey.name = name
        survey.result=survey.calculate_survey_result()
        return survey
class MessageTypes(Enum):
    TEXT = 'text'
    MULTIMEDIA=  'multimedia'
    ACTIVITY = 'activity'
class Message(EmbeddedDocument):
    type = EnumField(MessageTypes)
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
class EmotionTag(EmbeddedDocument):
    tag= StringField(required=True)
    score = FloatField(default=0.5)
class EmotionTagGroup(EmbeddedDocument):
    tags = SortedListField(EmbeddedDocumentField(EmotionTag),ordering="score",reverse = True)
    time_recorded= DateTimeField(default=datetime.utcnow)
class EmotionProfile(EmbeddedDocument):
    time_recorded = DateTimeField(default=datetime.utcnow)
    full_score = FloatField(required=True)
    chat_score = FloatField(required=True)
    latest_emotions = EmbeddedDocumentField(EmotionTagGroup)
class EmotionProfileList(EmbeddedDocument):
    time_started = DateTimeField(default=datetime.utcnow)
    profile_list = SortedListField(EmbeddedDocumentField(EmotionProfile),ordering="time_recorded",reverse = True)
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
    utc_in_hours=FloatField(default=0.0)
    previous_emotion_profile_lists = SortedListField(EmbeddedDocumentField(EmotionProfileList),ordering="time_started",reverse = True)
    latest_emotion_profile :EmotionProfile = EmbeddedDocumentField(EmotionProfile,default=lambda: EmotionProfile(full_score=0.5,chat_score=0.5)) 
    surveys = SortedListField(EmbeddedDocumentField(Survey),ordering="time_submitted",reverse = True)
    preferences = SortedListField(EmbeddedDocumentField(Preference),ordering="score",reverse = True)
    pred_preferences = SortedListField(EmbeddedDocumentField(Preference),ordering="score",reverse = True)
    latest_conversation_uuid = StringField()
    activities_emotion= StringField(default='neutral')
    activities_change_positive_threshold=FloatField(default=0.5)
    activities_change_negative_threshold=FloatField(default=0.5)
    _survey_period = -1
    def get_emotion_profile_copy(self):
        pf = self.latest_emotion_profile
        emotion_profile = EmotionProfile(full_score=pf.full_score,chat_score=pf.chat_score,latest_emotions=pf.latest_emotions)
        return emotion_profile

    def get_most_confident_emotion(self):
        emotion_tag = self.latest_emotion_profile.latest_emotions
        return emotion_tag.tags[0].tag


class Conversation(Document):
    time_started = DateTimeField(default=datetime.utcnow, required=True)
    time_ended = DateTimeField()
    uuid = StringField()
    user = ReferenceField(User,reverse_delete_rule=CASCADE)
    content = SortedListField(EmbeddedDocumentField(Message),ordering="time_sent",reverse = True)

class Statistic(EmbeddedDocument):
    users_average_full_score = FloatField()
    users_average_chat_score = FloatField()
    time_recorded = DateTimeField(default=datetime.utcnow, required=True)
class GlobalStatistics(Document):
    statistics: List[Statistic] = SortedListField(EmbeddedDocumentField(Statistic),ordering="time_recorded",reverse = True)
    def get_recent_statistic(self):
        if not self.statistics:
            return Statistic(users_average_full_score=0.5,users_average_chat_score=0.5)
        return self.statistics[0]
    @staticmethod
    def calculate_global_statistics(users: List[User]):
        stat = Statistic()
        stat.users_average_full_score = statistics.fmean(map(lambda user:user.latest_emotion_profile.full_score,users))
        stat.users_average_chat_score = statistics.fmean(map(lambda user:user.latest_emotion_profile.chat_score,users))
        return stat





