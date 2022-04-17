from mongoengine import *
from mongoengine.fields import BooleanField, EmbeddedDocumentField, EmbeddedDocumentListField, IntField, ListField, ReferenceField, SortedListField
from datetime import datetime
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
_sentiment_intensity_analyzer = SentimentIntensityAnalyzer()
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

class EmotionScore(EmbeddedDocument):
    time_recorded = DateTimeField(default=datetime.utcnow)
    full_score = FloatField(required=True)
    chat_score = FloatField(required=True)
class EmotionScoreList(EmbeddedDocument):
    time_started = DateTimeField(default=datetime.utcnow)
    score_list = SortedListField(EmbeddedDocumentField('EmotionScore'),ordering="time_recorded",reverse = True)
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
    previous_emotion_score_lists = SortedListField(EmbeddedDocumentField('EmotionScoreList'),ordering="time_started",reverse = True)
    emotion_score = EmbeddedDocumentField('EmotionScore',default=EmotionScore(full_score=0.5,chat_score=0.5))
    surveys = SortedListField(EmbeddedDocumentField('Survey'),ordering="time_submitted",reverse = True)
    preferences = SortedListField(EmbeddedDocumentField('Preference'),ordering="score",reverse = True)
    pred_preferences = SortedListField(EmbeddedDocumentField('Preference'),ordering="score",reverse = True)
    latest_conversation_uuid = StringField()
    _survey_period = -1
    def get_new_emotion_score(user,message):
        assert User._survey_period != -1
        LOWEST_SURVEY_FACTOR=0.4
        HIGHEST_SURVEY_FACTOR=0.8
        PREVIOUS_CHAT_SCORE_WEIGHT = 0.8
        previous_chat_score = user.emotion_score.chat_score
        previous_full_score = user.emotion_score.full_score

        sentiment_result  = _sentiment_intensity_analyzer.polarity_scores(message)
        current_message_score = sentiment_result['compound']
        current_message_score = (current_message_score+1)/2

        new_emotion_chat_score =  previous_chat_score * PREVIOUS_CHAT_SCORE_WEIGHT  + current_message_score * (1-PREVIOUS_CHAT_SCORE_WEIGHT)

        latest_survey_score = 0.5
        normalized_time_since_last_survey=0
        if user.surveys:
            latest_survey_score = user.surveys[0].result 
            normalized_time_since_last_survey = max((datetime.utcnow() - user.surveys[0].time_submitted).total_seconds()/User._survey_period,1)
        survey_factor = LOWEST_SURVEY_FACTOR + (HIGHEST_SURVEY_FACTOR-LOWEST_SURVEY_FACTOR) * (1-normalized_time_since_last_survey) if normalized_time_since_last_survey else 0
        new_emotion_full_score = survey_factor * latest_survey_score + (1-survey_factor)* new_emotion_chat_score
        return EmotionScore(full_score = new_emotion_full_score, chat_score= new_emotion_chat_score)

class Conversation(Document):
    time_started = DateTimeField(default=datetime.utcnow, required=True)
    time_ended = DateTimeField()
    uuid = StringField()
    user = ReferenceField('User',reverse_delete_rule=CASCADE)
    content = SortedListField(EmbeddedDocumentField('Message'),ordering="time_sent",reverse = True)






