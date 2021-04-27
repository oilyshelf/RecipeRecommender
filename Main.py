# -*- coding: utf-8 -*-
"""RestApi/Main file

 Using Flask and Flask-RESTful creating a rest-api to communicate with google`s dialogflow
 also the entry point to the recipeRecommender

@authors Rostislav Iskandirov(oilyshelf), Ali Gökkaya(ScarxFace06)
"""

from flask import Flask, request
from flask_restful import Resource, Api
from RecommenderPackage import Recommender

# Set up flask, restful and the recommender

app = Flask(__name__)
api = Api(app)

USERPROFILE = 4
recom = Recommender(USERPROFILE)
DYNAMIC = True


class HelloWorld(Resource):
    """
     A simple testing Rest api call returning a hello world json obj
    """

    def get(self):
        return {'Hallo': 'Welt'}


class Webhook(Resource):
    """
    The Webhook class is used to for the google calls
    """

    def post(self):
        """post request methode

        :return: tuple (response:json-obj, http-response-code)
        """
        some_json = request.get_json()
        print(some_json)
        return self._switch(some_json), 201

    def _switch(self, json):
        """this function determines which action is send by google´s dialogflow and creates the right response

        :param json:
        :return: a google dialogflow conform json response
        """
        action = json['queryResult']['action']
        session = json['session']

        response = {'fulfillmentText': 'This is a response from webhook.'}
        if action == 'rezept.wunsch':
            if recom.user.is_user():
                response = {
                    'fulfillmentMessages': [{'text':
                                                 {'text': [next(recom)]}
                                             }],
                    'outputContexts': [
                        {'name': session + '/contexts/rezept_wahl', 'lifespanCount': 1}]
                }
            else:
                response = {
                    'fulfillmentMessages': [{'text':
                                                 {'text': [
                                                     'Zur Einrichtung deines Profils, beantworte mir bitte ein paar fragen, hast du irgendwelche Allergien und wenn ja welche ?']}
                                             }],
                    'outputContexts': [
                        {'name': session + '/contexts/rezept_wunsch', 'lifespanCount': 1}]
                }

        elif action == 'allergien.wahl':
            temp = json['queryResult']['parameters']['Allergies']
            if len(temp) == 0:
                response['fulfillmentText'] = 'Du hast also keine Allergien?'
            else:
                response['fulfillmentText'] = " ".join(temp) + (
                    ' sind also deine Allergien?' if len(temp) > 1 else ' ist also deine Allergie?')
        elif action == 'Allergien.Allergien-yes':
            recom.user.set_allergies(json['queryResult']['parameters']['Allergies'])
            print(recom.user.allergies)
            response = {
                'fulfillmentText': 'Ok hast du irgendeine besondere Ernährungsweise ?',
                'followupEvent': 'tags_wahl'
            }
        elif action == 'Allergien.Allergien-no':
            response = {
                'fulfillmentText': 'Ok, bitte wiederhole deine Allergien',
                'followupEvent': 'allergien_wahl'
            }

        elif action == 'tags_wahl':
            temp = json['queryResult']['parameters']['Tags']
            if len(temp) == 0:
                response['fulfillmentText'] = 'Du hast also keine besondere Ernährungsweise'
            else:
                response['fulfillmentText'] = " ".join(temp) + ' ist also deine besondere Ernährungsweise?'
        elif action == 'Tags.Tags-yes':
            recom.user.set_tags(json['queryResult']['parameters']['Tags'])
            print(recom.user.preferred_tags)
            response = {
                'fulfillmentText': 'Ok hast du einen Thermomixer ?'

            }
        elif action == 'Tags.Tags-no':
            response = {
                'fulfillmentText': 'Ok bitte wiederhole deine besondere Ernährungsweise',
                'followupEvent': 'tags_wahl'
            }

        elif action == 'thermomix-yes':
            response = self.thermo_intent(True, session)
        elif action == 'thermomix-no':
            response = self.thermo_intent(False, session)
        elif action == "rezept-yes":
            recom.end_session()
            response = recom.recipe_card()
        elif action == "rezept-no":
            response = {
                'fulfillmentMessages': [{'text':
                                             {'text': [next(recom)]}
                                         }],
                'outputContexts': [
                    {'name': session + '/contexts/rezept_wahl', 'lifespanCount': 1}]
            }

        elif action == 'Zutaten.Zutaten-no':
            response = self.ing_intent(False, session, json)

        elif action == 'Zutaten.Zutaten-yes':
            response = self.ing_intent(True, session, json)

        elif action == 'rezept.aehnlich':
            ing = json['queryResult']['parameters']['Ingredients']
            extra = json['queryResult']['parameters']['ohne_mit']
            extra = False if extra == "0" else True
            recom.get_hybrid(extra=extra, ingredient=ing)
            response = {
                'fulfillmentMessages': [{'text':
                                             {'text': [next(recom)]}
                                         }],
                'outputContexts': [
                    {'name': session + '/contexts/rezept_wahl', 'lifespanCount': 1}]
            }

        return response

    def thermo_intent(self, has, session):
        """
        to prevent redundant code the action taken by answering this question only differ by the setting data to either true or false

        :param:  has:bool  , session:string
        :return: response:jsonstring
        """
        recom.user.set_thermo(has)
        if DYNAMIC:
            ingredient = recom.dynamic()

            return {
                'fulfillmentMessages': [{'text':
                                             {'text': ['Ok, magst du ' + ingredient + ' ?']}
                                         }],
                'outputContexts': [
                    {'name': session + '/contexts/zutaten-followup', 'lifespanCount': 1}]
            }
        else:
            return {
                'fulfillmentMessages': [{'text':
                                             {'text': ['Ok, nenn mir bitte ein paar Zutaten die dir nicht gefallen']}
                                         }],
                'outputContexts': [
                    {'name': session + '/contexts/thermomix_gewaehlt', 'lifespanCount': 1}]
            }

    def ing_intent(self, chosen, session, json):
        """
        to prevent redundant code the action taken by answering this question only differ by the setting data to either true or false

        :param:  chosen:bool  , session:string, json:jsonstring
        :return: response:jsonstring
        """

        if DYNAMIC:
            if ingredient := recom.dynamic(likes=chosen):
                return {
                    'fulfillmentMessages': [{'text':
                                                 {'text': ['Ok, magst du ' + ingredient + ' ?']}
                                             }],
                    'outputContexts': [
                        {'name': session + '/contexts/zutaten-followup', 'lifespanCount': 1}]
                }
            else:
                return {
                    'fulfillmentText': ' Ok dein Profil wurde erstellt, frage mich bitte noch einmal nach einem Rezeptvorschlag'
                }

        else:
            if not chosen:
                return {
                    'fulfillmentMessages': [{'text':
                                                 {'text': ['Ok, wiederhole bitte die Zutaten nochmal']}
                                             }],
                    'outputContexts': [
                        {'name': session + '/contexts/thermomix_gewaehlt', 'lifespanCount': 1}]
                }
            else:
                recom.user.set_disliked_ing(json['queryResult']['parameters']['ingredients'])
                recom.create_userprofile(recom.user)
                return {
                    'fulfillmentText': ' Ok dein Profil wurde erstellt, frage mich bitte noch einmal nach einem Rezeptvorschlag'
                }


# add classes to the rest api

api.add_resource(HelloWorld, '/')
api.add_resource(Webhook, '/webhook')

if __name__ == '__main__':
    app.run(debug=True)
