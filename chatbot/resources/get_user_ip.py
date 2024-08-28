from flask_restful import Resource
from flask import request
import json
from server.server import r


class GetUserIP(Resource):

    def get(self):
        device_type = request.args.get('deviceType', 'Desktop')
        device_detail = request.args.get('deviceDetail', 'Desktop')
        session_id = request.args.get('sessionId', '')

        dealer_id = request.args.get('dealerId', '2019123456001')
        dealer_name = request.args.get('dealerName', 'telle')

        ip_addr = request.remote_addr

        message = {
            'deviceType': device_type,
            'deviceDetail': device_detail,
            'sessionId': session_id,
            'dealerId': dealer_id,
            'dealerName': dealer_name,
            'ip_addr': ip_addr
        }

        message_data = json.dumps({'type': 'UPDATE_USER',
                                   'dealerId': dealer_id,
                                   'groupId': session_id,
                                   'message': message})

        r.rpush('telle:queue:daemon', message_data)

        return {
                   'isError': False,
                   'message': 'user page view has been added',
                   'statusCode': 200
               }, 200

        # return update_user(message)
