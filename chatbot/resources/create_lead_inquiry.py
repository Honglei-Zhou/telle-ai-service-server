from flask_restful import Resource
from flask import request
import json
from server.server import r
from server.config import service_channel
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class CreateLeadInquiry(Resource):

    def post(self):

        logger.info(request)

        dealerId = request.form.get('dealerId', '2019123456001')
        title = request.form.get('title', '')
        price = request.form.get('price', '')
        customer = request.form.get('customer', 'customer')
        email = request.form.get('email', '')
        phone = request.form.get('phone', '')
        zipcode = request.form.get('zipcode', '')
        vin = request.form.get('vin', '')
        stock = request.form.get('stock', '')
        sessionId = request.form.get('sessionId', '')
        new_message = {
            'dealerId': dealerId,
            'customer': customer,
            'email': email,
            'phone': phone,
            'note': '',
            'zipcode': zipcode,
            'vin': vin,
            'stock': stock,
            'sessionId': sessionId,
            'title': title,
            'price': price
        }

        message_data = json.dumps({'type': 'CREATE_LEAD_INQUIRY',
                                   'dealerId': dealerId,
                                   'groupId': sessionId,
                                   'message': new_message})
        r.publish(service_channel,
                  json.dumps({'type': 'UPDATE_NOTIFICATION',
                              'dealerId': dealerId,
                              'groupId': sessionId,
                              'customer': customer,
                              'department': 'sales'}))

        r.rpush('telle:queue:notification', message_data)
        r.rpush('telle:queue:daemon', message_data)
        return json.dumps({
            'isError': False,
            'message': 'leads has been created',
            'statusCode': 200
        })
