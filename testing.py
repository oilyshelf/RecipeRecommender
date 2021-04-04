# -*- coding: utf-8 -*-
"""Unit-testing Module

purely for testing Units

@authors Rostislav Iskandirov(oilyshelf), Ali Gökkaya(ScarxFace06)
"""
from RecommenderPackage import Recommender
from RecommenderPackage import DataBase






if __name__ == '__main__':
    r = Recommender()
    # r.user.set_disliked_ing(['Eier'])
    # r.user.set_thermo(True)
    # r.user.set_tags(['laktosefrei'])
    # r.user.set_allergies([])
    # r.create_userprofile(r.user)
    # print(next(r))
    # c = r.contend_recommender(r.user.last[0])
    # cb = next(c)
    # print('org rezept',r.user.last[0],'recommended',cb)
    # print(r.db.recipe_response((cb,100)))
    # db = DataBase()
    # print(db.bool_df.head())
    # print(db == r.db)

    print(r.dynamic())
    if text := r.dynamic(likes=False):
        print(text)
    print(r.user.is_user())