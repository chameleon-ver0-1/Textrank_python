from flask_restful import Resource

from service.keyword import Keyword
from service.summary import Summary
from util.parser import Parser


class MakeSummary(Resource):
    def post(self):
        try:
            # Parse HTTP Body
            parser = Parser(['roomId'])
            args = parser.get_args()

            # Read whole log data
            # FIXME: Read from DB
            filepath = 'text4.txt'

            # Abstract summary, keywords
            summary_stop_word = [('있', 'VV'), ('하', 'VV'), ('되', 'VV')]
            keyword_stop_word = [('있', 'VV'), ('하', 'VV'), ('되', 'VV'), ('없', 'VV')]

            summary = Summary(filepath, summary_stop_word).run()
            keyword = Keyword(filepath, keyword_stop_word).run()

            return {'status': 'res.status_code', 'message': 'res.text'}

        except Exception as e:
            return {'status': '500', 'message': f'{e}'}


class TestFlask(Resource):
    def post(self):
        try:
            return {'status': '200', 'message': 'hello!'}

        except Exception as e:
            return {'status': '500', 'message': f'{e}'}
