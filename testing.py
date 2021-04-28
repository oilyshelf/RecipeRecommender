# -*- coding: utf-8 -*-
"""Unit-testing Module

purely for testing Units

@authors Rostislav Iskandirov(oilyshelf), Ali Gökkaya(ScarxFace06)
"""
from RecommenderPackage import Recommender
from RecommenderPackage import DataBase
from flask import Flask, jsonify
import os



def recommender_test(print_recom = True):

    for _id in range(5):

        r = Recommender(_id)
        if _id == 0:
            r.set_user_info(0, ["tomaten"])
            r.set_user_info(1, ["Milch"])
            r.set_user_info(2, ["quick, laktsoefrei"])
            r.set_user_info(3, False)
            #test the creation process
            print(r.check_user())
            r.create_userprofile()
        print(r.check_user())
        print(r.user)

        for i in range(2000):
            print(next(r)) if print_recom else next(r)

        r.get_hybrid(extra=True, ingredient=["Reis"],preci=70)

        for i in range(71):
            print(next(r)) if print_recom else next(r)
        r.end_session()

        for i in range(200):
            print(next(r)) if print_recom else next(r)
        
        r.get_hybrid(extra=False, ingredient=["Karotte"],preci=10)

        for i in range(5):
            print(next(r)) if print_recom else next(r)
        
        r.end_session()

        for i in range(500):
            print(next(r)) if print_recom else next(r)
    print("____________________________________________________________")
    print("Recipe_Unit Test Done")

if __name__ == '__main__':
    recommender_test(print_recom=False)