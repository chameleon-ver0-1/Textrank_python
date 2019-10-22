from pymongo import MongoClient


class MongoReader:
    def __init__(self, room_id):
        self._room_id = room_id

    def read_topic_n_content(self):
        try:
            db = MongoClient('mongodb://localhost/')

            cursor = db['develop']['logs'].find({'roomId': self._room_id}).sort("createdAt")

            topics = []
            contents = {}
            contents_temp = {}

            for log in cursor:
                if log['topic'] == 'undefined':
                    continue

                tag = log['topic']

                if tag not in topics:
                    topics.append(tag)
                    contents_temp[tag] = []

                contents_temp[tag].append(log['content'])

            for topic in topics:
                contents['topic'] = '.\n'.join(contents_temp[topic]) + '.'

            print('======reader======')
            print(topics)
            print(contents)

            return topics, contents

        except Exception as e:
            print(e)
            return False, False

