import logging
from flask_cors import CORS
from server.server import app, r
from flask_restful import Api
# from server.listener import Listener
# from server.config import service_channel
from chatbot.resources import (CreateLeadPost, CreateLeadIntent, UpdateLeadIntent, CreateLeadInquiry,
                               GetUserIP, UpdateUserPageView, CreateApptFromIntent)
# import json

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

app.config['SECRET_KEY'] = 'secret!'
CORS(app)

api = Api(app)

'''
room map format: 
{
room_key: {user: [session_id], bot: [session_id], admin: [session_id], muted: True}
}
'''


api.add_resource(GetUserIP, '/api/user/ip')
api.add_resource(UpdateUserPageView, '/api/user/pageview')

api.add_resource(CreateLeadPost, '/api/create_lead')
api.add_resource(CreateLeadIntent, '/api/create_new_lead')
api.add_resource(UpdateLeadIntent, '/api/update_new_lead')
api.add_resource(CreateLeadInquiry, '/api/inquiry_stock')
api.add_resource(CreateApptFromIntent, '/api/create_new_appt')


@app.route('/hello')
def hello():
    # r.publish(service_channel, json.dumps({'type': 'UPDATE_USER_IP', 'message': 'test message'}))
    return 'hello world haha'


if __name__ == '__main__':
    # client = Listener(r, [service_channel], app)
    # client.start()

    app.run(host='0.0.0.0', port=5002, debug=False)
