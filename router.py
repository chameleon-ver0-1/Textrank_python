from flask import Flask
from flask_restful import Api

app = Flask(__name__)
api = Api(app)

'''
    ROUTING METHOD
'''
api.add_resource('', '/notification/start')


if __name__ == "__main__":
    app.run()
