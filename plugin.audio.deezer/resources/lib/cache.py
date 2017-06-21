import cPickle as pickle
import os.path
import time
import xbmc

import logging

class Cache(object):
    TTL = 10 * 60  # 10 mins ttl

    def __init__(self, name):
        self.name = name
        self.is_loaded = False
        self.is_dirty = False
        self._cache = {}
        self.file = None

    def read_cache(self):
        if not self.is_loaded:
            path = xbmc.translatePath("special://temp/%s.p" % self.name)

            if os.path.isfile(path):
                self.file = open(path, 'r+')
                self._cache = pickle.load(self.file)
            else:
                self.file = open(path, 'w+')
                self._cache = {}

            self.is_loaded = True
        return self._cache

    @property
    def cache(self):
        return self.read_cache()

    def clear(self):
        self.read_cache()
        self._cache = {}

    def set(self, key, value, ttl=TTL):
        logging.error('set item %s', key)

        self.is_dirty = True
        self.cache[key.lower()] = {'time': time.time(), 'ttl': ttl, 'value': value}

    def has(self, key):
        key = key.lower()
        if key not in self.cache:
            return False
        else:
            item = self.cache[key]
            # if item's expiry time is in the past, remove it from cache
            if item['time'] + item['ttl'] < time.time():
                self.is_dirty = True
                del self.cache[key]
                return False
            else:
                return True

    def get(self, key, default_value=None, default_producer=None, ttl=TTL):
        logging.debug('read item %s', key)
        key = key.lower()
        if self.has(key):
            return self.cache[key]['value']
        if default_producer is not None:
            product = default_producer()
            self.set(key, product, ttl)
            return product
        return default_value

    def save(self):
        if self.is_dirty and self.file is not None:
            self.file.seek(0)
            pickle.dump(self.cache, self.file, protocol=-1)  # -1 will choose fastest version supported
