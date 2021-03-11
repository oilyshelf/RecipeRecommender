import RecommenderPackage.databaseConnection
import numpy as np
import pandas as pd
import RecommenderPackage.user

class Recommender:
    def __init__(self):
        # TODO init the recommender
        self.db = RecommenderPackage.databaseConnection.DataBase()
        self.user = RecommenderPackage.User()

    def know_recommender(self, user):
        res = self.db.bool_df.dot(user.profile)
        #1808 is the count of recipies
        for i in res.nlargest(1808).iteritems():
            yield i
    #TODO change to class solution

    def contend_recommender(self, recipe_id, cosine_similarity_matrix, df):
        index = df[df['recID'] == recipe_id].index.values[0]
        similarity_scores = list(enumerate(cosine_similarity_matrix[index]))
        similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
        # delete the first cuz it´s itself lol
        print(similarity_scores.pop(0))
        for i in similarity_scores:
            yield self.index_to_recipeID(i[0], df)

    def create_userProfile(self, user):
        #creating empty dataframe
        data = np.full([1, len(self.db.columns)], 0.25, dtype=np.float64)
        user_Profile = pd.DataFrame(data=data, columns=self.db.columns)
        for x in self.db.thermo.itertuples():
            user_Profile[x.Index] = 1.0 if user.theromix else 0.0
        if user.disliked_ing is not None:
            for x in user.disliked_ing:
                for i in self.db.ing_df[self.db.ing_df['info'].str.contains(x.lower())].itertuples():
                    #print('ing :', x, ' id info', i.Index, ' ', i.info)
                    user_Profile[i.Index] = 0

        if user.allergies is not None:
            for a in user.allergies:
                for i in self.db.alg_df[self.db.alg_df['info'].str.contains(a.lower())].itertuples():
                    #print('allergie :', a, ' id info', i.Index, ' ', i.info)
                    user_Profile[i.Index] = -1.0

        if user.prefered_tags is not None:
            for tag in user.prefered_tags:
                for i in self.db.tags_df[self.db.tags_df['info'].str.contains(tag.lower())].itertuples():
                    #print('tag :', tag, ' id info', i.Index, ' ', i.info)
                    user_Profile[i.Index] = 5.0
        user.set_userprofile(user_Profile)

    def index_to_recipeID(self, index, df):
        return df.loc[index]['recID']



#testing

if __name__ == '__main__':
    r = Recommender()
