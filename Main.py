from flask import Flask,request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'Hallo': 'Welt'}


class webhook(Resource):
    def post(self):
        some_json = request.get_json()
        print(some_json)
        response = {'fulfillmentText': 'This is a response from webhook.'}
        if some_json['queryResult']['action'] == 'zutaten.selector' :
            if some_json['queryResult']['parameters']['ingredients'] == 'Tomaten':
                response = {'fulfillmentText': 'schlechte wahl'}
            else:
                response = {'fulfillmentText': 'gute wahl'}



        return response, 201

api.add_resource(HelloWorld, '/')
api.add_resource(webhook,'/webhook')

if __name__ == '__main__':
    app.run(debug=True)