from random import randint, sample
from .dataclass import *
import logging
logger = logging.getLogger(__name__)
import random
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
_sentiment_intensity_analyzer = SentimentIntensityAnalyzer()
class Recommender():
    def check_if_recommend(user,message):
        PREVIOUS_WEIGHT = 0.8
        MAX_FREQ= 10
        MIN_FREQ= 5
        sentiment_result  = _sentiment_intensity_analyzer.polarity_scores(message)
        current_score = sentiment_result['compound']
        current_score = (current_score+1)/2
        user.emotion_score =  user.emotion_score * PREVIOUS_WEIGHT  + current_score * (1-PREVIOUS_WEIGHT)
        user.save()
        threshold=  (1/MIN_FREQ - 1/MAX_FREQ )*user.emotion_score + 1/MAX_FREQ

        return random.uniform(0,1) < threshold
    # 1- avg mean sq diff 
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
    def recommend(cls,username,num_of_top_items = 3):
        num_of_neighbors = 5
       
        current_user = User.objects(username=username).first()
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

        # add random items if predicted preferences lack members
        if remaining_items >0:            
            remaining_multimediadata = MultiMediaData.objects(name__not__in=list(map(lambda x:x.content.name,current_user.pred_preferences))).all()
            current_user.pred_preferences += [Preference(content=x,score=-1) for x in sample(list(remaining_multimediadata),k=remaining_items)]

        current_user.save()
        current_user = User.objects(username=username).first()

        idx = randint(0,num_of_top_items-1) if len(current_user.pred_preferences) >=num_of_top_items else (len(current_user.preferences) -1)
        
        return current_user.pred_preferences[idx].content,current_user.pred_preferences

        

