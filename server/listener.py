import threading
import logging
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Listener(threading.Thread):
    def __init__(self, r, channels, app):
        threading.Thread.__init__(self)
        self.daemon = True
        self.redis = r
        self.pubsub = self.redis.pubsub()
        self.pubsub.psubscribe(channels)
        self.app = app

    def work(self, item):
        with self.app.app_context():
            if isinstance(item['data'], bytes):
                try:
                    msg = item['data'].decode('utf-8')
                    decode_msg = json.loads(msg)
                    print(decode_msg)
                    if decode_msg['type'] == 'UPDATE_TASK':
                        print(decode_msg)
                except ValueError as e:
                    print("Error decoding msg to microservice: %s", str(e))

    def run(self):
        for item in self.pubsub.listen():
            self.work(item)
