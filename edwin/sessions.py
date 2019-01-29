# -*- coding: utf8 -*-

import redis
import json
import copy
from collections import OrderedDict

class Session(OrderedDict):
    _redispool = redis.ConnectionPool(host='127.0.0.1', port=6379, max_connections=100, db=4)
    _redisconn = redis.Redis(connection_pool=_redispool)

    def __init__(self, *args, **kwargs):
        super(Session, self).__init__(*args, **kwargs)

    def save(self, key):
        data = json.dumps(self)
        self._redisconn.set(key, data, ex=120, nx=True)

    @staticmethod
    def load(key):
        session = Session()
        if key is not None:
            data = Session._redisconn.get(key)
            if data is not None:
                data = json.loads(data)
                session.update(**data)
        return session

    def flush(self, key):
        self._redisconn.delete(key)