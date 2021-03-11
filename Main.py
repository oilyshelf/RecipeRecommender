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
        return self._switch(action), 201

    def _switch(self, action):
        response = {'fulfillmentText': 'This is a response from webhook.'}
        return response


api.add_resource(HelloWorld, '/')
api.add_resource(webhook, '/webhook')

if __name__ == '__main__':
    app.run(debug=True)
