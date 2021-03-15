import RecommenderPackage.databaseConnection
import numpy as np
import pandas as pd
import RecommenderPackage.user


class Recommender:
    def __init__(self):
        self.db = RecommenderPackage.databaseConnection.DataBase()
        self.user = RecommenderPackage.User()

    def __next__(self):
        if self.user.gen is None:
            self.user.set_gen(self.know_recommender(self.user))
        res = next(self.user.gen)
        self.user.last = res
        return self.db.recipe_response(res)

    def know_recommender(self, user):
        # 1808 is the count of recipies
        for i in self.db.bool_df.dot(user.profile).nlargest(1808).iteritems():
            yield i

    def contend_recommender(self, recipe_id):
        df = self.db.feature_set_df
        cosine_similarity_matrix = self.db.cosine_similarity_matrix_count_based
        index = df[df['recID'] == recipe_id].index.values[0]
        # delete the first cuz it´s itself lol
        for i in sorted(list(enumerate(cosine_similarity_matrix[index])), key=lambda x: x[1], reverse=True)[1:]:
            yield self.index_to_recipe_id(i[0])

    def hybrid_recommender(self, recipe_id):
        # todo creating an df with the top picks from the contend_recommender and then filter them with
        #  a knowledge_based approach to get specific results
        return

    def create_userprofile(self, user):
        # creating empty dataframe
        data = np.full([1, len(self.db.columns)], 0.25, dtype=np.float64)
        user_profile = pd.DataFrame(data=data, columns=self.db.columns)
        for x in self.db.thermo.itertuples():
            user_profile[x.Index] = 1.0 if user.theromix else -1.0
        if user.disliked_ing is not None:
            for x in user.disliked_ing:
                for i in self.db.ing_df[self.db.ing_df['info'].str.contains(x.lower())].itertuples():
                    # print('ing :', x, ' id info', i.Index, ' ', i.info)
                    user_profile[i.Index] = 0

        if user.allergies is not None:
            for a in user.allergies:
                for i in self.db.alg_df[self.db.alg_df['info'].str.contains(a.lower())].itertuples():
                    # print('allergie :', a, ' id info', i.Index, ' ', i.info)
                    user_profile[i.Index] = -1.0

        if user.prefered_tags is not None:
            for tag in user.prefered_tags:
                for i in self.db.tags_df[self.db.tags_df['info'].str.contains(tag.lower())].itertuples():
                    # print('tag :', tag, ' id info', i.Index, ' ', i.info)
                    user_profile[i.Index] = 5.0
        user.set_userprofile(user_profile.iloc[0])

    def index_to_recipe_id(self, index):
        return self.db.feature_set_df.loc[index]['recID']

    def recipe_card(self):
        return self.db.recipe_card(self.user.last)
