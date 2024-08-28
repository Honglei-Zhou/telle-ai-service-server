from flask_restful import Resource
from flask import request
import json
from server.server import r
from server.config import service_channel
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class UpdateLeadIntent(Resource):

    def get(self):
        logger.info(request)
        email = request.args.get('email')
        phone = request.args.get('phone')
        session_id = request.args.get('sessionId')
        dealer_id = request.args.get('dealerId', '2019123456001')
        department = request.args.get('department')
        customer = request.args.get('customer')
        message = {}
        if phone:
            message['phone'] = phone
        if email:
            message['email'] = email
        if session_id:
            message['sessionId'] = session_id
        if dealer_id:
            message['dealerId'] = dealer_id
        if department:
            message['department'] = department
        if customer:
            message['customer'] = customer

        message_data = json.dumps({'type': 'UPDATE_LEAD_INTENT',
                                   'dealerId': dealer_id,
                                   'sid': session_id,
                                   'message': message})
        r.publish(service_channel,
                  json.dumps({'type': 'UPDATE_NOTIFICATION',
                              'dealerId': dealer_id,
                              'groupId': session_id,
                              'customer': customer,
                              'department': department}))

        r.rpush('telle:queue:notification', message_data)

        r.rpush('telle:queue:daemon', message_data)

        return json.dumps({
            'isError': False,
            'message': 'leads has been created',
            'statusCode': 200
        })
