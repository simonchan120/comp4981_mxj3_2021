from random import randint
from dataclass import *
import logging
logger = logging.getLogger(__name__)
class Recommender():
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
        top_k_neighbors_score_list = neighbors_score_list[:num_of_neighbors]
        
        
        preference_list = cls._predict_scores(current_user,top_k_neighbors_score_list)
        current_user.pred_preferences = current_user.preferences + preference_list
        current_user.save()

        current_user = User.objects(username=username).first()

        idx = randint(0,num_of_top_items-1) if len(current_user.pred_preferences) >=num_of_top_items else (len(current_user.preferences) -1)
        
        return current_user.pred_preferences[idx].content,current_user.pred_preferences

        

