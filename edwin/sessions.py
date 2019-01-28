# -*- coding: utf8 -*-

import redis
import json
from collections import OrderedDict

class Session(OrderedDict):
    _redispool = redis.ConnectionPool(host='127.0.0.1', port=6379, max_connections=100, db=4)
    _redisconn = redis.Redis(connection_pool=_redispool)

    def save(self, key):
        data = json.dumps(self)
        self._redisconn.set(key, data, ex=120, nx=True)

    def load(self, key):
        data = self._redisconn.get(key)
        if data is not None:
            data = json.loads(data)
            self.update(**data)

    def flush(self):
        self._redisconn.delete()