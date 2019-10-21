from flask_restful import reqparse


class Parser:
    def __init__(self, args: list):
        self._parser = reqparse.RequestParser()
        for arg in args:
            self._parser.add_argument(arg, type=str)

    def get_args(self):
        return self._parser.parse_args()
