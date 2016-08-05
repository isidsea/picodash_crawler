from lib.location_data   import LocationData
from lib.picodash.engine import Picodash
from lib.media.saver     import MediaSaver
from lib.exceptions      import LoginErrorException, DuplicateData
from selenium            import webdriver
from pymongo             import MongoClient
import selenium
import bson.json_util
import multiprocessing
import pymongo
import pyprind

def callback(media=None):
	assert media is not None, "media is not defined."
	try:
		media_saver = MediaSaver()
		media_saver.save(media)
		print("[picodash_crawler] Inserted one document!")
	except pymongo.errors.DuplicateKeyError:
		print("[picodash_crawler] Ops! Duplicate Data! {}".format(media["PostCreated_Time"]))
		raise DuplicateData("Duplicate data on database.")

	# print(bson.json_util.dumps(media, indent=4, separators=(",",":")))
#end def

def execute_thread(data=None):	
	current       = multiprocessing.current_process()
	db            = MongoClient("mongodb://mongo:27017/test")
	db            = db.monitor
	location_data = LocationData()

	try:	
		assert data is not None, "data is not defined."
		print("[picodash_crawler] Engine start!")

		db.pico_worker.update({"name":current.name},{"$set":{
			  "name" : current.name,
			"status" : "working"
		}},upsert=True)

		location = data[0]
		cookies  = data[1]
		location_data.set_as_processing(location)

		picodash         = Picodash()
		picodash.cookies = cookies
		picodash.apply_cookies()
		picodash.crawl(location_data=location, callback=callback)

		location_data.set_as_processed(location)
	except AssertionError:
		print("[picodash_crawler] Assertion is not satisfied.")
	finally:
		db.pico_worker.update({"name":current.name},{"$set":{
			  "name" : current.name,
			"status" : "finished"
		}},upsert=True)		
		print("[picodash_crawler] Crawler DEAD!")

if __name__ == "__main__":
	picodash = Picodash()
	picodash.login()

	location_data = LocationData()
	locations     = location_data.get_locations()
	print("[picodash_crawler] Number of Locations: {}".format(len(locations)))
	
	locations     = [(location, picodash.cookies) for location in locations]
	multi_process = multiprocessing.Pool(10)
	multi_process.map(execute_thread, locations)
