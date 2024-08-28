from flask_restful import Resource
from flask import request
import json
from server.server import r
from server.config import service_channel
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class CreateApptFromIntent(Resource):

    def post(self):

        logger.info(request)

        keys = {
            "VehicleType": "VehicleType",
            "VehicleDrivetrain": "VehicleDrivetrain",
            "VehicleBudget": "VehicleBudget",
            "VehicleColor": "VehicleColor",
            "VehicleMake": "VehicleMake",
            "VehicleModel": "VehicleModel",
            "VehicleFeatures": "VehicleFeatures",  # list
            "VehicleYear": "VehicleYear",
            "test_drive_date": "test_drive_date",
            "test_drive_time": "test_drive_time",
            "person": "person",  # dict
            "email": "email",
            "phone-number": "phone-number",
            "sessionId": "sessionId"
        }

        message = {}
        for key in keys:
            val = request.form.get(key)
            if val:
                message[key] = val

        dealer_id = request.form.get('dealerId', '2019123456001')

        message['dealerId'] = dealer_id

        message_data = json.dumps({'type': 'CREATE_APPT_INTENT',
                                   'dealerId': dealer_id,
                                   'groupId': message['sessionId'],
                                   'message': message})

        r.publish(service_channel,
                  json.dumps({'type': 'UPDATE_NOTIFICATION',
                              'dealerId': dealer_id,
                              'groupId': message['sessionId'],
                              'customer': message['person'],
                              'department': 'sales'}))

        r.rpush('telle:queue:notification', message_data)
        r.rpush('telle:queue:daemon', message_data)

        return json.dumps({
            'isError': False,
            'message': 'leads has been created',
            'statusCode': 200
        })
