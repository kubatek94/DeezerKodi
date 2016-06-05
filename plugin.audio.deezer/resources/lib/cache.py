import cPickle as pickle
import os.path
import time
import xbmc

class Cache(object):
	TTL = 60*60 #1 hour ttl

	def __init__(self, name):
		self.name = xbmc.translatePath("special://temp/%s.p" % name) 
		self.epoch = time.time()
		if os.path.isfile(self.name):
			self.cache = pickle.load(open(self.name, "rb"))
		else:
			self.cache = {}

	def set(self, key, value, ttl=TTL):
		key = key.lower()
		self.cache[key] = {'time' : self.epoch, 'ttl' : ttl, 'value' : value}

	def has(self, key):
		key = key.lower()
		if key not in self.cache:
			return False
		else:
			item = self.cache[key]
			#if item lives longer than ttl allowes, remove it from cache
			if (item['time'] + item['ttl']) > self.epoch:
				del self.cache[key]
				return False
			else:
				return True

	def get(self, key, default_value=None, default_producer=None, ttl=TTL):
		if self.has(key):
			return self.cache[key]['value']
		if default_producer is not None:
			product = default_producer()
			self.set(key, product, ttl)
			return product
		return default_value

	def save(self):
		pickle.dump(self.cache, open(self.name, "wb"))
