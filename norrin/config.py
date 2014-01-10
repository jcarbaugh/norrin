import os
from urlparse import urlparse

UA_KEY = os.environ.get('UA_KEY')
UA_SECRET = os.environ.get('UA_SECRET')
UA_MASTER = os.environ.get('UA_MASTER')
AUTORELOAD_SUBSCRIBERS = os.environ.get('AUTORELOAD_SUBSCRIBERS', False)

SENTRY_DSN = os.environ.get('SENTRY_DSN')

mongohq_url = os.environ.get('MONGOHQ_URL')

if mongohq_url:
    o = urlparse(mongohq_url)
    MONGODB_HOST = o.hostname
    MONGODB_PORT = o.port
    MONGODB_DATABASE = o.path.lstrip('/')
    MONGODB_USERNAME = o.username
    MONGODB_PASSWORD = o.password
else:
    MONGODB_HOST = os.environ.get('MONGODB_HOST', 'localhost')
    MONGODB_PORT = os.environ.get('MONGODB_PORT', 27017)
    MONGODB_DATABASE = os.environ.get('MONGODB_DATABASE', 'norrin')
    MONGODB_USERNAME = os.environ.get('MONGODB_USERNAME')
    MONGODB_PASSWORD = os.environ.get('MONGODB_PASSWORD')
