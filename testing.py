import sqlite3
import sys, os
from RecommenderPackage import Recommender




if __name__ == '__main__':
    r = Recommender()
    r.user.set_disliked_Ing(['Eier'])
    r.user.set_thermo(True)
    r.user.set_tags(['laktosefrei'])
    r.user.set_allergies([])
    r.create_userprofile(r.user)
    print(next(r))
    c = r.contend_recommender(r.user.last[0])
    cb = next(c)
    print('org rezept',r.user.last[0],'recommended',cb)
    print(r.db.recipe_response((cb,100)))

