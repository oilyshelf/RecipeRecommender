import sqlite3
import sys, os
from RecommenderPackage import Recommender




if __name__ == '__main__':
    r = Recommender()
    print(r.db.bool_df.head())
