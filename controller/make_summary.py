from flask_restful import Resource

from util.parser import Parser


parser = Parser(['roomId'])


class MakeSummary(Resource):
    def post(self):
        try:

            args = parser.get_args()

            title = f"[{args['roomId']}] 에서 {args['task']} 작업 시작"
            detail = args['detail']

            return {'status': 'res.status_code', 'message': 'res.text'}

        except Exception as e:
            return {'status': '500', 'message': '알림 실패'}