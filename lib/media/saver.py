from pymongo import MongoClient
from ..      import tools

class MediaSaver(object):
	def __init__(self):
		self.db = None
		self.db = MongoClient("mongodb://hotp:hotp7890@220.100.163.134:27017/test?authSource=hotp")
		self.db = self.db.hotp

		tools._force_create_index(self.db, "picodash_test", "PostUrl")

	def save(self, media=None):
		assert self.db    is not None, "db is not defined."
		assert media      is not None, "media is not defined."

		self.db.picodash_test.insert_one(media)


