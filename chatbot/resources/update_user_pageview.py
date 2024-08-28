from flask_restful import Resource
from flask import request
import json
from server.server import r
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class UpdateUserPageView(Resource):

    def post(self):
        logger.info(request)
        ip_addr = request.remote_addr
        session_id = request.form.get('sessionId')
        page = request.form.get('page')
        dealer_id = request.form.get('dealerId', '2019123456001')
        bot_clicked = request.form.get('botClicked', '0')

        message = {
            'sessionId': session_id,
            'dealerId': dealer_id,
            'ip_addr': ip_addr,
            'page': page,
            'bot_clicked': int(bot_clicked)
        }

        if session_id is None or len(session_id) < 3 or page is None or len(page) < 5:
            return {
                    'isError': True,
                    'message': 'Empty message',
                    'statusCode': 200,
                    }, 200

        message_data = json.dumps({'type': 'UPDATE_USER_PV',
                                   'dealerId': dealer_id,
                                   'sid': session_id,
                                   'message': message})

        r.rpush('telle:queue:daemon', message_data)

        return {
                   'isError': False,
                   'message': 'user page view has been added',
                   'statusCode': 200
               }, 200
