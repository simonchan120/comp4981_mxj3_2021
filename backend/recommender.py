from random import randint
from dataclass import *
class Recommender():
    # 1- avg mean sq diff 
    def _knn_sim(user_a,user_b):
        
        se = []
        for a_key,a_value in user_a.preferences.dict_pairs.items():
            for b_key,b_value in user_b.preferences.dict_pairs.items():
                    if b_key == a_key:
                        se.append((a_value-b_value)*(a_value-b_value))
        if len(se) <= 0:
            return None
        mse = sum(se)/len(se)
        return mse

    # aggregation approach: average
    def _predict_scores(user, top_k_neighbors_score_list):
        
        preference_list = []
        for multimedia in MultiMediaData.objects():
            if user.preferences(content=multimedia).front() is not None:
                continue
            item_scores = []
            for key,value in top_k_neighbors_score_list:
                preference = top_k_neighbors_score_list[1].preferences(content=multimedia).first()

                
                if preference is not None:
                    item_scores.append(preference.score)
            if len(item_scores) != 0:
                score = item_scores/len(item_scores)
                preference_list.append(Preference(multimedia,item_scores))
        return preference_list

    @classmethod
    def recommend(cls,username):
        num_of_neighbors = 5
        current_user = User.objects(username=username).first()
        users=User.objects()
        neighbors_score_list = []
        for user in users:
            result= cls._knn_sim(current_user,user)
            if result is not None:
                neighbors_score_list.push(result,user)
        neighbors_score_list.sort(key = lambda x: int(x[0]),reverse=True)
        top_k_neighbors_score_list = neighbors_score_list[:num_of_neighbors]
        
        
        preference_list = cls._predict_scores(current_user,top_k_neighbors_score_list)
        current_user.preferences += preference_list



        num_of_top_items = 5
        idx = randint(0,num_of_top_items-1) if len(current_user.preferences) >=num_of_top_items else len(current_user.preferences)
        return current_user.preferences[idx]

        

