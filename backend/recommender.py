from dataclasses import dataclass
from random import randint, sample
from .data.dataclass import User, EmotionProfile, MultiMediaData, Preference, EmotionTagGroup, EmotionTag, Message, MessageTypes
import logging
logger = logging.getLogger(__name__)
import random
from datetime import datetime
from backend import goemotions
# import nltk
# nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
_sentiment_intensity_analyzer = SentimentIntensityAnalyzer()
from backend import giphy_util

class Recommender():


    @staticmethod
    def calculate_new_emotion_profile(user:User,message):
        assert User._survey_period != -1
        LOWEST_SURVEY_FACTOR=0.4
        HIGHEST_SURVEY_FACTOR=0.8
        PREVIOUS_CHAT_SCORE_WEIGHT = 0.8
        previous_chat_score = user.latest_emotion_profile.chat_score
        previous_full_score = user.latest_emotion_profile.full_score

        sentiment_result  = _sentiment_intensity_analyzer.polarity_scores(message)
        current_message_score = sentiment_result['compound']
        current_message_score = (current_message_score+1)/2

        new_emotion_chat_score =  previous_chat_score * PREVIOUS_CHAT_SCORE_WEIGHT  + current_message_score * (1-PREVIOUS_CHAT_SCORE_WEIGHT)

        latest_survey_score = 0.5
        normalized_time_since_last_survey=0
        if user.surveys:
            latest_survey_score = user.surveys[0].result 
            normalized_time_since_last_survey = min((datetime.utcnow() - user.surveys[0].time_submitted).total_seconds()/User._survey_period,1)
        survey_factor = LOWEST_SURVEY_FACTOR + (HIGHEST_SURVEY_FACTOR-LOWEST_SURVEY_FACTOR) * (1-normalized_time_since_last_survey) if normalized_time_since_last_survey else 0
        new_emotion_full_score = survey_factor * latest_survey_score + (1-survey_factor)* new_emotion_chat_score
        
        emotion_tags_and_scores  = goemotions(message)[0]
        emotion_tag_list=[EmotionTag(tag=tag,score=score) for tag,score in zip(emotion_tags_and_scores['labels'],emotion_tags_and_scores['scores'])]
        emotion_tag_group = EmotionTagGroup(tags=emotion_tag_list)
        return EmotionProfile(full_score = new_emotion_full_score, chat_score= new_emotion_chat_score,latest_emotions=emotion_tag_group)

    @staticmethod
    def check_if_recommend_multimedia(user: User,message):

        MAX_FREQ= 1/5
        MIN_FREQ= 1/10
        
        full_emotion_score = user.latest_emotion_profile.full_score
        threshold=  (MAX_FREQ - MIN_FREQ)*full_emotion_score + MIN_FREQ

        return random.uniform(0,1) < threshold
    @staticmethod
    def check_if_recommend_activities(user: User,message, save_user=True):
        POS_THRESHOLD_LOWEST=NEG_THRESHOLD_LOWEST=0.3
        POS_THRESHOLD_HIGHEST=NEG_THRESHOLD_HIGHEST = 1.0
        STEP_FACTOR=0.3
        # NEUTRAL_SKIP_THRESHOLD =0.5
        polarity_scores=_sentiment_intensity_analyzer.polarity_scores(message)

        # if polarity_scores['neu'] >= NEUTRAL_SKIP_THRESHOLD:
        #     return False
        logger.debug(f"{message=}:{polarity_scores=}")
        negativity_score = polarity_scores['neg']
        positivity_score = polarity_scores['pos']
        if negativity_score <= POS_THRESHOLD_LOWEST and positivity_score <=POS_THRESHOLD_HIGHEST:
            return False
        assert NEG_THRESHOLD_LOWEST <= user.activities_change_negative_threshold and user.activities_change_negative_threshold <= NEG_THRESHOLD_HIGHEST 
        assert POS_THRESHOLD_LOWEST <= user.activities_change_positive_threshold and user.activities_change_positive_threshold <= POS_THRESHOLD_HIGHEST 
        is_neg = negativity_score > positivity_score and negativity_score >= user.activities_change_negative_threshold
        is_pos = positivity_score > negativity_score and positivity_score <= user.activities_change_positive_threshold
        is_recommend = is_neg or is_pos 

        logger.debug(f"For user : {user.username=},{negativity_score=},{positivity_score=},{POS_THRESHOLD_LOWEST=},{POS_THRESHOLD_HIGHEST=},{NEG_THRESHOLD_LOWEST=},{NEG_THRESHOLD_HIGHEST=},{is_neg=},{is_pos=}")
        logger.debug(f"Before: {user.activities_change_negative_threshold=},{user.activities_change_positive_threshold=}")
        if is_recommend:
            if negativity_score > positivity_score:
                diff = NEG_THRESHOLD_HIGHEST - user.activities_change_negative_threshold
                user.activities_change_negative_threshold += diff*STEP_FACTOR
            else:
                diff =  user.activities_change_positive_threshold -POS_THRESHOLD_LOWEST 
                user.activities_change_positive_threshold -= diff*STEP_FACTOR
        else:
            if negativity_score > positivity_score:
                diff = user.activities_change_negative_threshold - NEG_THRESHOLD_LOWEST
                user.activities_change_negative_threshold -= diff*STEP_FACTOR
            else:
                diff = POS_THRESHOLD_HIGHEST-user.activities_change_positive_threshold
                user.activities_change_positive_threshold += diff*STEP_FACTOR
        logger.debug(f"After: {user.activities_change_negative_threshold=},{user.activities_change_positive_threshold=}")
        if save_user:
            user.save()
        return is_recommend
    # 1- avg mean sq diff 
    @staticmethod
    def _knn_sim(user_a,user_b):
        
        se = []
        for a_preference in user_a.preferences:
            for b_preference in user_b.preferences:
                    if a_preference.content == b_preference.content:
                        se.append((a_preference.score-b_preference.score)*(a_preference.score-b_preference.score))
        if len(se) <= 0:
            return None
        mse = sum(se)/len(se)
        return mse

    # aggregation approach: average
    @staticmethod
    def _predict_scores(user, top_k_neighbors_score_list):
        
        preference_list = []
        for multimedia in MultiMediaData.objects():
            if any(multimedia==pref.content for pref in user.preferences):
                continue
            item_scores = []
            for score_neighbor,user_neighbor in top_k_neighbors_score_list:
                
                neighbor_preference = None
                for item in user_neighbor.preferences:
                    if item.content == multimedia:
                        neighbor_preference = item
                        break

                
                if neighbor_preference is not None:
                    item_scores.append(neighbor_preference.score)
            if len(item_scores) != 0:
                score = sum(item_scores)/len(item_scores)
                preference_list.append(Preference(content = multimedia,score = score))
        return preference_list
    @classmethod
    def recommend_activities(cls,current_user: User):
        return current_user.get_most_confident_emotion()
    @classmethod
    def recommend_multimedia(cls,current_user: User,num_of_top_items = 3,save_user=True):
        num_of_neighbors = 5
        users=User.objects()
        neighbors_score_list = []
        for user in users:
            result= cls._knn_sim(current_user,user)
            if result is not None:
                neighbors_score_list.append((result,user))
        neighbors_score_list.sort(key = lambda x: int(x[0]),reverse=True)

        #fails if knn list is less than num of neighbors
        
        top_k_neighbors_score_list = neighbors_score_list[:num_of_neighbors] if len(neighbors_score_list) > num_of_neighbors else neighbors_score_list
               
        preference_list = cls._predict_scores(current_user,top_k_neighbors_score_list)


        current_user.pred_preferences = current_user.preferences + preference_list
        
        remaining_items = num_of_top_items - len(current_user.pred_preferences)

        # 5% chance for recommending all random items
        if random.uniform(0,1) <= 0.05:
            remaining_items = num_of_top_items
            current_user.pred_preferences = []

        # add random items if predicted preferences lack members
        if remaining_items >0:            
            remaining_multimediadata = MultiMediaData.objects(name__not__in=list(map(lambda x:x.content.name,current_user.pred_preferences))).all()
            current_user.pred_preferences += [Preference(content=x,score=-1) for x in sample(list(remaining_multimediadata),k=remaining_items)]

        # current_user = User.objects(username=current_user.username).first()

        idx = randint(0,num_of_top_items-1) if len(current_user.pred_preferences) >=num_of_top_items else (len(current_user.preferences) -1)
        logger.debug(f'{[x.content.name for x in current_user.pred_preferences]}, index: {idx}, no of origianlly existing items: {num_of_top_items-remaining_items}, no of added items: {remaining_items}')
        if save_user:
            current_user.save()
        return current_user.pred_preferences[idx].content,current_user.pred_preferences

    @staticmethod
    def process_message(user,user_message,current_conversation,response_obj,save_user=True):
        user.latest_emotion_profile= Recommender.calculate_new_emotion_profile(user,user_message)
        if Recommender.check_if_recommend_multimedia(user,user_message):
            multimedia,_ = Recommender.recommend_multimedia(user,save_user=False)
            giphy_tag = multimedia.name

            logger.debug(f'User: {user.username}, Recommended: {giphy_tag}')
            #TODO: more types
            giphy_link,_ = giphy_util.fetch_multimedia(giphy_tag)
            response_obj.append({'type':'gif','url':giphy_link,'name':giphy_tag})
            recommender_message_obj=Message(content=giphy_link,is_from_user=False, type=MessageTypes.MULTIMEDIA)
            current_conversation.content.append(recommender_message_obj)

            #swap order to allow message to go last
            current_conversation.content[0], current_conversation.content[1] = current_conversation.content[1],current_conversation.content[0]
            response_obj[0],response_obj[1] = response_obj[1],response_obj[0]
        if Recommender.check_if_recommend_activities(user,user_message,save_user=False):
            activity_emotion_tag = Recommender.recommend_activities(user)
            response_obj.append({'type':'emotion_tag','tag':activity_emotion_tag})
            recommender_message_obj= Message(content=activity_emotion_tag, is_from_user=False, type=MessageTypes.ACTIVITY)
        if save_user:
            user.save()
        return

