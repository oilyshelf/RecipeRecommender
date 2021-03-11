from flask import Flask, request
from flask_restful import Resource, Api

from RecommenderPackage import Recommender

app = Flask(__name__)
api = Api(app)

recom = Recommender()


class HelloWorld(Resource):
    def get(self):
        return {'Hallo': 'Welt'}


class webhook(Resource):
    def post(self):
        some_json = request.get_json()
        print(some_json)
        action = some_json['queryResult']['action']
        return self._switch(action, some_json), 201

    def _switch(self, action, json):
        response = {'fulfillmentText': 'This is a response from webhook.'}
        if(action == 'DefaultWelcomeIntent.Rezeptwunsch'):
            response = {'fulfillmentText': 'ok nenne mir bitte ein Paar Zutaten die dir nicht gefallen'}
        elif action == 'zutaten.selector':
            text = 'ok du magst also keine '+"".join(json['queryResult']['parameters']['ingredients']) + " hab ich dich richtig verstanden ?"
            response = {'fulfillmentText': text}
        elif action == 'zutaten.selector.DefaultWelcomeIntent-Rezeptwunsch-Zutaten-no':
            response = {"followupEventInput": {'name': 'DefaultWelcomeIntent-Rezeptwunsch'}}

        return response


api.add_resource(HelloWorld, '/')
api.add_resource(webhook, '/webhook')

if __name__ == '__main__':
    app.run(debug=True)
