# -*- coding: utf-8 -*-
"""Unit-testing Module

purely for testing Units

@authors Rostislav Iskandirov(oilyshelf), Ali Gökkaya(ScarxFace06)
"""
from RecommenderPackage import Recommender
from RecommenderPackage import DataBase
from flask import Flask, jsonify
import os



if __name__ == '__main__':
    r = Recommender()
    r.user.set_disliked_ing(['Eier'])
    r.user.set_thermo(True)
    r.user.set_tags(['laktosefrei'])
    r.user.set_allergies([])
    r.create_userprofile(r.user)
    # print(next(r))
    # c = r.contend_recommender(r.user.last[0])
    # cb = next(c)
    # print('org rezept',r.user.last[0],'recommended',cb)
    # print(r.db.recipe_response((cb,100)))

    next(r)
    l = r.user.last
    print(r.db.recipe_response(l))

    r.get_hybrid( extra=False,ingredient=['karotte'])
    print("_____________________ohne Karrotte____________")
    print(next(r))
    print("________________mit tomate und reis______________________________")
    r.get_hybrid( extra=True,ingredient=['reis', "tomate"])
    print("--------------------------------------------------------hybrid loop start---------------------------------------------------------------")
    for i in range(21):
        print(next(r))
        print("_______________________________________________________________________________________________________________________________")

    # c = r.contend_recommender(r.user.last[0])
    # l = [next(c) for i in range(20)]
    # print(l)
    # test = r.db.bool_df.loc[l]
    # r.hybrid_recommender(r.user.last[0], preci=20)

    

    # print(r.dynamic())
    # if text := r.dynamic(likes=False):
    #     print(text)
    # print(r.user.is_user())