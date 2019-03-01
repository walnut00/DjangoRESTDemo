# -*- coding: utf8 -*-

import redis
import json
import copy
from collections import OrderedDict
from threading import local

class Session(OrderedDict):
    _redispool = redis.ConnectionPool(host='127.0.0.1', port=6379, max_connections=100, db=4)
    _redisconn = redis.Redis(connection_pool=_redispool)
    _local = local() # threading.local，线程变量，保持各个线程的独立

    def __init__(self, *args, **kwargs):
        super(Session, self).__init__(*args, **kwargs)
        self._local.changed = False

    def save(self, key):
        data = json.dumps(self)
        #self._redisconn.set(key, data, ex=1200, nx=True)
        self._redisconn.set(key, data, ex=3600)
        self._local.changed = False

    @staticmethod
    def load(key):
        session = Session()
        if key is not None:
            data = Session._redisconn.get(key)
            if data is not None:
                data = json.loads(data)
                session.update(**data)

        session.changed = False
        return session

    def flush(self, key):
        self._redisconn.delete(key)

    @property
    def changed(self):
        return self._local.changed

    @changed.setter
    def changed(self, value):
        self._local.changed = value

    def __setitem__(self, key, value):
        super(Session, self).__setitem__(key, value)
        self._local.changed = True
