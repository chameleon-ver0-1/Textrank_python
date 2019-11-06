from flask_restful import Resource

import traceback
import requests
import json

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
            room_id = args['roomId']
            reader = MongoReader(room_id)
            topics, p_contents = reader.read_topic_n_content()

            # TODO: 예지 : 주제별요약&키워드가 담길 배열 변수 --> 이부분이 요청으로 들어갈 2개의 변수 아래 예시데이터보면 확인할 수 있음
            contents = []
            keywords = []

            # Abstract summary, keywords
            summary = {}
            keyword = {}

            summary_stop_word = set([
                ('있', 'VV'), ('웃', 'VV'), ('와우', 'IC'), ('시작', 'NNG'), ('협조', 'NNG'), ('하', 'VV'), ('되', 'VV'),
                ('이','VCP'), ('것','NNB'), ('들','XSN'), ('그','MM'), ('수','NNB'), ('이','NP'), ('보','VX'), ('않','VX'),
                ('없','VA'), ('나','NP'), ('주','VV'), ('아니','VCN'), ('등','NNB'), ('같','VA'), ('우리','NP'), ('때','NNG'),
                ('년','NNB'), ('가','VV'), ('한','MM'), ('지','VX'), ('대하','VV'), ('오', 'VV'),('그렇','VA'),('위하','VV'),('그것','NP'),('두','VV'),('그러나','MAJ'),('못하','VX'),('그런','MM'),('또','MAG'),('더','MAG'),('그리고','MAJ'),('중','NNB'),('씨','NNB'),('지금','NNG'),('그러','VV'),('속','NNG'),('데','NNB'),('안','MAG'),('어떤','MM'),('내','NP'),('다시','MAG'),('이런','MM'),('번','NNB'),('나','VX'),('어떻','VA'),('개','NNB'),('이렇','VA'),('점','NNG'),('좀','MAG'),('잘','MAG'),('이빨','NNG')])
    
            keyword_stop_word = set([('있', 'VV'), ('웃', 'VV'),('와우', 'IC'),('시작', 'NNG'), ('협조', 'NNG'),('하', 'VV'), ('되', 'VV'),('이','VCP'),('것','NNB'),('들','XSN'),('그','MM'),('수','NNB'),('이','NP'),('보','VX'),('않','VX'),('없','VA'),('나','NP'),('주','VV'),('아니','VCN'),('등','NNB'),('같','VA'),('우리','NP'),('때','NNG'),('년','NNB'),('가','VV'),('한','MM'),('지','VX'),('대하','VV'),('오','VV'),('그렇','VA'),('위하','VV'),('그것','NP'),('두','VV'),('그러나','MAJ'),('못하','VX'),('그런','MM'),('또','MAG'),('더','MAG'),('그리고','MAJ'),('중','NNB'),('씨','NNB'),('지금','NNG'),('그러','VV'),('속','NNG'),('데','NNB'),('안','MAG'),('어떤','MM'),('내','NP'),('다시','MAG'),('이런','MM'),('번','NNB'),('나','VX'),('어떻','VA'),('개','NNB'),('이렇','VA'),('점','NNG'),('좀','MAG'),('잘','MAG'),('이빨','NNG')])

            for topic in topics:
                if topic not in p_contents:
                    continue

                text = p_contents[topic]

                summary_temp = Summary(text, summary_stop_word).run()
                keyword_temp = Keyword(text, keyword_stop_word).run()

                print(' -*-*- SEMI-TEMP -*-*- ')
                print(summary_temp)
                print(keyword_temp)

                summary[topic] = summary_temp
                keyword[topic] = keyword_temp

                print(' -*-*- SEMI-RESULT -*-*- ')
                print(summary[topic])
                print(keyword[topic])

                # TODO: 예지 - 주제별 요약
                contents.append({
                    "topic": topic,
                    "content": summary_temp
                })

                # TODO: 예지 - 주제별 키워드
                # 전체 합 구한 다음 각각의 값에서 sum을 나누고 100을 곱해 비율계산한 뒤 자연수로 변환
                total = 0
                for val in keyword_temp.values():
                    total += val

                for key, val in keyword_temp.items():
                    keywords.append({
                        "keyword": f"{key[0][0]}",
                        "value": int((val/total)*100)
                    })

            # TODO: 소영아 내가 느려서 미안해 파이썬을 잘못하는 나의 잘못이야 이렇게 메모를 남겨

            # TODO: 예시 데이터 형식
            # {
            #    "keywords":[
            #    {
            #        "keyword":"지후",
            #        "value":15
            #    },
            #    {
            #        "keyword":"예지",
            #        "value":8
            #        
            #    }
            #    ],
            #    "contents":[
            #        {
            #            "topic":"소영이는 정말 대단해",
            #            "content":"소영이 화이팅"
            #        },
            #        {
            #            "topic":"윤영이는 너무 똑똑해",
            #            "content":"윤영이 거짓말쟁이"
            #        },
            #        {
            #            "topic":"예지는 언제쯤 그만 똑똑할까",
            #            "content":"지후 미안"
            #        }
            #    ]
            #}
            print('==== Conference Log Summary ====')
            print(summary)
            print(keyword)

            res = requests.post(f'https://a.chameleon4switch.cf/api/conf_log/create/{room_id}', data=json.dumps({
                "keywords": keywords,
                "contents": contents
            }))

            return {
                'status': res.status_code,
                'message': res.text
            }

        except Exception as e:
            print(e)
            print(traceback.format_exc())
            return {'status': '500', 'message': f'{e}'}


class TestFlask(Resource):
    def post(self):
        try:
            return {'status': '200', 'message': 'hello!'}

        except Exception as e:
            return {'status': '500', 'message': f'{e}'}
