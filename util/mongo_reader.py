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

            for log in cursor:
                if 'topic' not in log or log['topic'] == 'undefined' or log['topic'] == 'system':
                    continue

                tag = log['topic']
                contents_temp = []

                if tag not in topics:
                    topics.append(tag)

                contents_temp.append(log['content'])
                contents[tag] = '. '.join(contents_temp[tag]) + '.'

            print('======reader======')
            print(topics)
            print(contents)

            return topics, contents

        except Exception as e:
            print(e)
            return False, False

