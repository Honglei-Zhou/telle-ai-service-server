from flask import Flask
from server.config import db_string, redis_host, redis_port
import os
from werkzeug.middleware.proxy_fix import ProxyFix
import redis

path = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_string
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.wsgi_app = ProxyFix(app.wsgi_app)

r = redis.Redis(host=redis_host, port=redis_port)
