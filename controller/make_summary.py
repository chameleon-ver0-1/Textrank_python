from flask_restful import Resource

from service.keyword import Keyword
from service.summary import Summary
from util.mongo_reader import MongoReader
from util.parser import Parser


class MakeSummary(Resource):
    def post(self):
        try:
            # Parse HTTP Body
            parser = Parser(['roomId'])
            args = parser.get_args()

            # Read whole log data
            # FIXME: Read from DB
            room_id = args['roomId']
            reader = MongoReader(room_id)
            topics, contents = reader.read_topic_n_content()

            filepath = 'text4.txt'

            # Abstract summary, keywords
            summary = {}
            keyword = {}

            summary_stop_word = [('있', 'VV'), ('하', 'VV'), ('되', 'VV')]
            keyword_stop_word = [('있', 'VV'), ('하', 'VV'), ('되', 'VV'), ('없', 'VV')]

            for topic in topics:
                if topic not in contents:
                    continue

                text = contents[topic]

                summary[topic] = Summary(text, summary_stop_word).run()
                keyword[topic] = Keyword(text, keyword_stop_word).run()

                print(' -*-*- SEMI-RESULT -*-*- ')
                print(summary[topic])
                print(keyword[topic])

            # FIXME: 예지언니 여기서 API 기록 부탁해 사랑해 하트하트
            print('==== Conference Log Summary ====')
            print(summary)
            print(keyword)

            return {
                'status': 'res.status_code',
                'data': {
                    'topics': topics,
                    'summary': summary,
                    'keyword': keyword
                },
                'message': 'done!'
            }

        except Exception as e:
            print(e)
            return {'status': '500', 'message': f'{e}'}


class TestFlask(Resource):
    def post(self):
        try:
            return {'status': '200', 'message': 'hello!'}

        except Exception as e:
            return {'status': '500', 'message': f'{e}'}
