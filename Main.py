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

recom = Recommender()


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

        response = {'fulfillmentText': 'This is a response from webhook.'}
        if action == 'rezept.wunsch':
            if recom.user.is_user():
                response = next(recom)
            else:
                response = {
                    'fulfillmentText': 'Zur Einrichtung deines Profils, nenne mir bitte ein paar Zutaten, welche du nicht magst',
                    "followupEvent": {
                        'name': 'zutaten_wahl'
                    }}
        elif action == 'Zutaten.Zutaten-no':
            response = {
                'fulfillmentText': 'Ok, bitte wiederhole die Zutaten',
                "followupEvent": 'zutaten_wahl'
            }
        elif action == 'Zutaten.Zutaten-yes':
            recom.user.set_disliked_ing(json['queryResult']['parameters']['ingredients'])
            print(recom.user.disliked_ing)
            response = {
                'fulfillmentText': 'Ok, hast du irgendwelche Allergien und wenn ja welche ?',
                "followupEvent": 'allergien_wahl'
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
            recom.user.set_thermo(True)
            recom.create_userprofile(recom.user)
            response[
                'fulfillmentText'] = ' Ok dein Profil wurde erstellt, frage mich bitte noch einmal nach einem Rezeptvorschlag'
        elif action == 'thermomix-no':
            recom.user.set_thermo(False)
            recom.create_userprofile(recom.user)
            response[
                'fulfillmentText'] = ' Ok dein Profil wurde erstellt, frage mich bitte noch einmal nach einem Rezeptvorschlag'
        elif action == "rezept-yes":
            response = recom.recipe_card()
        elif action == "rezept-no":
            response = next(recom)

        return response


# add classes to the rest api
api.add_resource(HelloWorld, '/')
api.add_resource(Webhook, '/webhook')

if __name__ == '__main__':
    app.run(debug=True)
