from flask import Flask
from flask_restful import Api

from controller.make_summary import MakeSummary
from controller.make_summary import TestFlask


app = Flask(__name__)
api = Api(app)


'''
    ROUTING METHOD
'''
api.add_resource(MakeSummary, '/summary')
api.add_resource(TestFlask, '/test')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8282)
