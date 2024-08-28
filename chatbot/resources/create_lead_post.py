from flask_restful import Resource
from flask import request
import json
from server.server import r
from server.config import service_channel
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class CreateLeadPost(Resource):

    def post(self):
        logger.info(request)
        dealer_id = request.form.get('dealerId', '2019123456001')
        customer = request.form.get('customer', 'customer')
        email = request.form.get('email', '')
        phone = request.form.get('phone', '')
        note = request.form.get('note', '')
        session_id = request.form.get('sessionId', '')
        new_message = {
            'dealerId': dealer_id,
            'customer': customer,
            'email': email,
            'phone': phone,
            'note': note,
            'sessionId': session_id
        }

        message_data = json.dumps({'type': 'UPDATE_LEAD',
                                   'dealerId': dealer_id,
                                   'groupId': session_id,
                                   'message': new_message})

        r.publish(service_channel,
                  json.dumps({'type': 'UPDATE_NOTIFICATION',
                              'dealerId': dealer_id,
                              'groupId': session_id,
                              'customer': customer,
                              'department': 'sales'}))

        r.rpush('telle:queue:notification', message_data)
        r.rpush('telle:queue:daemon', message_data)

        return json.dumps({
            'isError': False,
            'message': 'leads has been created',
            'statusCode': 200
        })
