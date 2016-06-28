import json

class Config(object):
	def __init__(self):
		self._config = None
		self.read()

	@property
	def config(self):
		if type(self._config) is dict:
			return self._config
		else:
			return dict()
	

	def read(self):
		f           = open("/root/app/config.json","r")		
		self._config = json.load(f)		