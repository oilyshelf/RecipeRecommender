# -*- coding: utf-8 -*-
"""Database Module

holds Database-class which manages all access to Data from the Database and saved CSV-files
providing additional functions related to get Information from Data-sources
The Database-class is a singleton so all modules using this module are connected to the same data


@authors Rostislav Iskandirov(oilyshelf), Ali Gökkaya(ScarxFace06)
"""

import sqlite3
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import os


class DataBase(object):
    __instance = None

    def __new__(cls):
        if DataBase.__instance is None:
            cls.__instance = super(DataBase, cls).__new__(cls)
            # init here
            cls.__instance._inti()
        return cls.__instance

    def _inti(self):
        """This is a costume __init__ methode used to manage the singleton pattern
            this function should not be used else where

        :return nothing:
        """
        path = os.path.realpath('.\Resources\Data')
        print(path)

        # connection to the sqlite and cursor

        con = sqlite3.connect(path + '/RecipeDB.db')
        cur = con.cursor()

        # load Dataframes and create needed Dataframes
        bool_df = pd.read_csv(path + "/recipeBool.csv")
        bool_df.index = bool_df["Unnamed: 0"]
        bool_df = bool_df.drop(["Unnamed: 0"], axis=1)
        columns = bool_df.columns

        feature_set_df = pd.read_csv(path + '/recipe_feature_set.csv')
        feature_set_df.index = feature_set_df['Unnamed: 0']
        feature_set_df = feature_set_df.drop(["Unnamed: 0"], axis=1)

        dy_df = pd.read_csv(path + '/dynamic.csv')
        dy_df.index = dy_df['Unnamed: 0']
        dy_df = dy_df.drop(["Unnamed: 0"], axis=1)

        # creating helping df´s for finden id´s

        # func to normalize text
        def process_text(text):
            # replace muliple spaces with one
            text = ''.join(text.split())
            # lowercase
            text = text.lower()
            return text

        ing_df = pd.read_sql("Select ingID, ingName, familyName FROM Ingredients NATURAL JOIN IngFamily", con)
        ing_df.index = ing_df['ingID']
        ing_df['info'] = ing_df['ingName'] + " " + ing_df['familyName']
        ing_df = ing_df.drop(['ingName'], axis=1)
        ing_df = ing_df.drop(['familyName'], axis=1)
        ing_df = ing_df.drop(['ingID'], axis=1)

        ing_df['info'] = ing_df.apply(lambda x: process_text(x.info), axis=1)

        tags_df = pd.read_sql("Select * from Tags", con)
        tags_df.index = tags_df["tagID"]
        tags_df['info'] = tags_df['tagName'] + ' ' + tags_df['tagType']
        tags_df = tags_df.drop(["tagID"], axis=1)
        tags_df = tags_df.drop(["tagName"], axis=1)
        tags_df = tags_df.drop(["tagType"], axis=1)
        tags_df['info'] = tags_df.apply(lambda x: process_text(x.info), axis=1)

        alg_df = pd.read_sql("Select * from Allergens", con)
        alg_df.index = alg_df["alleID"]
        alg_df['info'] = alg_df['alleType'] + ' ' + alg_df['alleName'] + ' ' + alg_df['alleSlug']
        alg_df = alg_df.drop(["alleID"], axis=1)
        alg_df = alg_df.drop(["alleType"], axis=1)
        alg_df = alg_df.drop(["alleName"], axis=1)
        alg_df = alg_df.drop(["alleSlug"], axis=1)
        alg_df['info'] = alg_df.apply(lambda x: process_text(x.info), axis=1)

        thermo = tags_df[tags_df["info"].str.contains("thermomix")]

        # Matrices for the contentbased
        vect = CountVectorizer()

        vect_matrix = vect.fit_transform(feature_set_df['info'])

        cosine_similarity_matrix_count_based = cosine_similarity(vect_matrix, vect_matrix)

        # all needed Data and Dataframes
        self.bool_df = bool_df
        self.feature_set_df = feature_set_df
        self.ing_df = ing_df
        self.alg_df = alg_df
        self.tags_df = tags_df
        self.thermo = thermo
        self.cosine_similarity_matrix_count_based = cosine_similarity_matrix_count_based
        self.columns = columns
        self.path = path
        self.dy_df = dy_df
        # close db
        cur.close()
        con.close()

    def recipe_json(self, recipe_id):
        """Given a valid recipe_id this function creates with the help of the RecipeDB a json-obj containing
            all needed information

        :param recipe_id:string id of a recipe
        :return: A json obj containing all necessary Information
        """
        # create connection
        con = sqlite3.connect(self.path + '/RecipeDB.db')
        cur = con.cursor()
        res = {'id': recipe_id}
        sql = """ SELECT * FROM Recipe WHERE recID = ? ;"""
        recs = cur.execute(sql, (recipe_id,)).fetchall()[0]
        # basic infos
        res['name'] = recs[1]
        res['headline'] = recs[2]
        res['disc'] = recs[3]
        # ingredients
        recs = cur.execute(
            "SELECT ingID, ingName, familyID, familyName, amount, unit FROM IngInRec NATURAL JOIN Ingredients NATURAL JOIN IngFamily WHERE recID = ? ;",
            (recipe_id,)).fetchall()
        ingr = {}
        for ing in recs:
            ingr[ing[0]] = {'name': ing[1], 'amount': ing[4], 'unit': ing[5], 'family': {'id': ing[2], 'name': ing[3]}}
        res['ingredients'] = ingr

        # nutr
        recs = cur.execute("SELECT nType, amount, unit, nName FROM NutrInRec NATURAL JOIN Nutration WHERE recID = ? ;",
                           (recipe_id,)).fetchall()
        nutr = {}
        for i in recs:
            nutr[i[0]] = {'amount': i[1], 'unit': i[2], 'name': i[3]}
        res['nutration'] = nutr

        # allergene
        recs = cur.execute("SELECT alleID, alleName FROM AlleInRec NATURAL JOIN Allergens WHERE recID = ? ;",
                           (recipe_id,)).fetchall()
        alle = {}
        for i in recs:
            alle[i[0]] = i[1]
        res['allergies'] = alle

        # tags

        recs = cur.execute("SELECT tagID, tagName FROM TagsInRec NATURAL JOIN Tags WHERE recID = ? ;",
                           (recipe_id,)).fetchall()
        tags = {}
        for t in recs:
            tags[t[0]] = t[1]
        res['tags'] = tags

        # steps
        recs = cur.execute("SELECT stepIndex, stepDisc from StepsInRec WHERE recID = ?  ORDER BY stepIndex ;",
                           (recipe_id,)).fetchall()

        res['steps'] = [i[1] for i in recs]
        # close db
        cur.close()
        con.close()

        return json.dumps(res, indent=2, ensure_ascii=False)

    def recipe_response(self, rec):
        """Use to create a json response for googles dialogflow
            Uses the RecipeDB to get the name and description of an recipe

        :param rec: tuple with (recipe_id:string, score:float)
        :return: google dialogflow conform json obj representing an recipe
        """
        con = sqlite3.connect(self.path + '/RecipeDB.db')
        cur = con.cursor()
        # print(rec)
        title, descr = cur.execute('SELECT recName, recDisc From Recipe WHERE recID = ? ', (rec[0],)).fetchone()
        res = {
            'fulfillmentText': " Wie gefällt dir dieses Rezept : " + title + "," + descr + " es hatte ein Score von : " + str(
                rec[1])}
        # close db
        cur.close()
        con.close()
        return res['fulfillmentText']

    def recipe_card(self, rec):
        """Use to create a json response for googles dialogflow
            Uses the RecipeDB to get the name and image of an recipe

        :param rec: tuple with (recipe_id:string, score:float)
        :return: google dialogflow conform json obj representing an recipe including an image
        """
        con = sqlite3.connect(self.path + '/RecipeDB.db')
        cur = con.cursor()
        # print(rec)
        card, title = cur.execute('SELECT recLink,recName From Recipe WHERE recID = ? ', (rec[0],)).fetchone()
        res = {
            "fulfillmentMessages": [
                {
                    "card": {
                        "title": title,
                        "imageUri": card
                    }
                },
                {
                    "text": {
                        "text": [
                            "Folge bitte dem Link für die Rezeptzubereitung : '{}'  Guten Appetit mit {}".format(card, title)
                        ]
                    }
                }
            ]
        }
        # close db
        cur.close()
        con.close()
        return res

    def index_to_recipe_id(self, index):
        """ given an index from the similarity matrix determines the recipe_id

        :param index: int ( from matrix similarity matrix)
        :return:recipe_id : string
        """
        return self.feature_set_df.loc[index]['recID']

    def id_to_fam_name(self, fam_id):
        """returns family name of the given id
        :param: fam_id:string
        :return: name string
        """
        con = sqlite3.connect(self.path + '/RecipeDB.db')
        cur = con.cursor()
        res = cur.execute("Select familyName from IngFamily where familyID = ?", (fam_id,)).fetchone()[0]
        # close db
        cur.close()
        con.close()
        return res


    def family_to_ing(self, fam_id):
        """ return list of Ingredient names which are in the given family
        :param fam_id: string
        :return: List <string> 
        """
        con = sqlite3.connect(self.path + '/RecipeDB.db')
        cur = con.cursor()
        res = cur.execute("Select ingName from IngFamily NATURAL JOIN Ingredients where familyID = ?", (fam_id,)).fetchall()
        # close db
        cur.close()
        con.close()
        return [i[0] for i in res]
