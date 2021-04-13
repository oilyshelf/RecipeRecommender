# -*- coding: utf-8 -*-
"""Recommender-Module

contains the Recommender class which maneges users and create recommendations

@authors Rostislav Iskandirov(oilyshelf), Ali Gökkaya(ScarxFace06)
"""

import RecommenderPackage.databaseConnection
import numpy as np
import pandas as pd
import RecommenderPackage.user


class Recommender:
    def __init__(self):
        self.db = RecommenderPackage.databaseConnection.DataBase()
        self.user = RecommenderPackage.User(self.db.dy_df)

    def __next__(self):
        """
        costume __next__ methode to get an recipe recommendation
        first checks if user has an recommendation generator and creates on if not
        generates recommendation and safes it in user.last

        :return: a json response with an recipe recommendation
        """
        if self.user.gen is None:
            self.user.set_gen(self.know_recommender(self.user))
        
        res = None
        try:
            res = next(self.user.gen)
        except:
            print("reseting the generator")
            self.user.set_gen(self.know_recommender(self.user))
            res = next(self.user.gen)

        self.user.last = res
        return self.db.recipe_response(res)

    def know_recommender(self, user):
        """Generator for Knowledge based recommendations
            by creating a dot product with the user_profile and the bool_df determines the best scoring recipe to
            recommend the user
        :param user: User
        :return: tuple(recipe_id:string, score:float)
        """
        # 1808 is the count of recipes
        for i in self.db.bool_df.dot(user.profile).nlargest(1808).iteritems():
            yield i

    def contend_recommender(self, recipe_id):
        """Generator for contend based recommendations
        creates a recipe recommendation from a previously calculated similarity_matrix which is similar to
        given recipe_id

        :param recipe_id: string
        :return: recipe_id:string
        """
        df = self.db.feature_set_df
        cosine_similarity_matrix = self.db.cosine_similarity_matrix_count_based
        index = df[df['recID'] == recipe_id].index.values[0]
        # delete the first cuz it´s itself
        for i in sorted(list(enumerate(cosine_similarity_matrix[index])), key=lambda x: x[1], reverse=True)[1:]:
            yield self.db.index_to_recipe_id(i[0])

    def hybrid_recommender(self, recipe_id, profile, preci):
        g = self.contend_recommender(recipe_id)
        ids = [next(g) for i in range(preci)]

        hybrid_df = self.db.bool_df.loc[ids]
        for i in self.db.bool_df.dot(profile).nlargest(1808).iteritems():
            yield i


        # todo creating an df with the top picks from the contend_recommender and then filter them with
        #  a knowledge_based approach to get specific results
        return

    def create_userprofile(self, user):
        """creates with, in the User class saved preferences, a pandas series (to use for the recommenders) and saves
        it in the user

        :param user:User
        :return: None
        """
        # creating empty dataframe
        data = np.full([1, len(self.db.columns)], 0.25, dtype=np.float64)
        user_profile = pd.DataFrame(data=data, columns=self.db.columns)
        for x in self.db.thermo.itertuples():
            user_profile[x.Index] = 1.0 if user.theromix else -1.0
        if user.disliked_ing is not None:
            for x in user.disliked_ing:
                for i in self.db.ing_df[self.db.ing_df['info'].str.contains(x.lower())].itertuples():
                    # print('ing :', x, ' id info', i.Index, ' ', i.info)
                    user_profile.at[i.Index] = 0

        if user.allergies is not None:
            for a in user.allergies:
                for i in self.db.alg_df[self.db.alg_df['info'].str.contains(a.lower())].itertuples():
                    # print('allergie :', a, ' id info', i.Index, ' ', i.info)
                    user_profile.at[i.Index] = -1.0

        if user.preferred_tags is not None:
            for tag in user.preferred_tags:
                for i in self.db.tags_df[self.db.tags_df['info'].str.contains(tag.lower())].itertuples():
                    # print('tag :', tag, ' id info', i.Index, ' ', i.info)
                    user_profile.at[i.Index] = 5.0
        user.set_userprofile(user_profile.iloc[0])

    def recipe_card(self):
        """using an Database function return a google dialogflow json response
            only use to as an interface between the RestApi and the Database

        :return: a Json response with recipe info´s and an image
        """
        return self.db.recipe_card(self.user.last)

    def dynamic(self, likes=None):
        """
        TODO write documentation
        A function, which asks questions dynamically
        The next question changes according to the previous answer, therefore the dataframe for relevant recipes gets smaller
        after 5 questions, the most relevant recipe gets presented
        """
        self.user.counter +=1
        if self.user.counter == 5:
            self.create_userprofile(self.user)
            return False
        if likes is not None:
            self.user.update_df(likes)
            if not likes:
                self.user.extend_disliked(self.db.family_to_ing(self.user.last_ing))

        df = self.user.dataframe
        size = df.shape[0]
        percentage_list = [(str(i), df[df[i] == True].shape[0] / size) for i in df.columns]
        l = np.array([i[1] for i in percentage_list])
        idx = (np.abs(l - 0.5)).argmin()
        fam_id = percentage_list[idx]
        self.user.update_ing(fam_id[0])
        return self.db.id_to_fam_name(fam_id[0])

    def modify_userprofile(self,extra, ingredient):
        if ingredient is None:
            return self.user.profile
        
        profile = self.user.profile
        for x in ingredient:
            for i in self.db.ing_df[self.db.ing_df['info'].str.contains(x.lower())].itertuples():
                profile.at[i.Index] = 10.0 if extra else -10.0
        
        return profile

    def get_hybrid(self, extra = True, ingredient = None, preci = 20):
        self.user.gen = self.hybrid_recommender(self.user.last[0], self.modify_userprofile(extra,ingredient), preci)






