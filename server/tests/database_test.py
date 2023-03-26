from random import randint
from hashlib import md5
from json import dumps as json_dumps

from os import path as os_path
from sys import path as sys_path

directory = os_path.abspath(__file__)
sys_path.append( os_path.join(directory, "..", "..", "..") )

from server.utility.database import RobloxAnalytics

sys_path.pop()

def run_light_test() -> list[ (bool, str) ]:
	print("light test - start")
	TEST_RESULTS = []

	sample_data = { "Currency" : randint(1, 1e6), "Inventory" : [{"ID" : "1", "Quantity" : 1, "UUID" : "123123-123123-123123-123123"}] }
	
	print("light test - create files")
	simple_database = RobloxAnalytics(id="LIGHT_TEST")
	print("light test - set sample data")
	simple_database.SetValue("PlayerAnalytics1", "1", sample_data)
	print("light test - get sample data")
	stored_value = simple_database.GetValue("PlayerAnalytics1", "1")

	# save and load
	print("light test - hash comparison")
	saving_hash = md5(json_dumps(sample_data).encode()).hexdigest()
	loaded_hash = md5(json_dumps(stored_value).encode()).hexdigest()
	if saving_hash == loaded_hash:
		TEST_RESULTS.append((True, "Sample data was able to be saved and loaded. Hash Value: " + saving_hash))
	else:
		TEST_RESULTS.append((False, f"Failed to save and load. Got data hash {loaded_hash}, expected {saving_hash}"))

	print("light test - delete database")
	simple_database.delete()

	print("light test - ended")
	return TEST_RESULTS

def run_heavy_test() -> list[ (bool, str) ]:
	print("heavy test - start")
	
	def GetRandomInventoryData() -> dict:
		inventory = { }
		ids = [ "ItemID_" + str( randint(100, 10000) ) for _ in range(50) ]
		for _id in ids:
			inventory[_id] = { }
			uids = [ "UUID_" + str( randint(100, 10000) ) for _ in range(5) ]
			for _uid in uids:
				inventory[_id][_uid] = { "Quantity" : randint(1, 200) }
		return inventory

	print("heavy test - generating user ids")
	sample_user_ids = [ str(i) for i in range(1000) ]
	
	print("heavy test - generating user datas - ", len(sample_user_ids))
	sample_user_datas = [ {"Currency" : randint(100, 10000), "Inventory" : GetRandomInventoryData()} for _ in range( len(sample_user_ids) ) ]
	
	print("heavy test - generating files")
	bulk_database = RobloxAnalytics(id="HEAVY_TEST")
	
	print("heavy test - database bulk set")
	bulk_database.SetBulkValue("PlayerAnalytics1", sample_user_ids, sample_user_datas)
	
	print("heavy test - delete sample database")
	bulk_database.delete()

	print("heavy test - ended")
	return [ (True, "Heavy Test was successful") ]

if __name__ == '__main__':
	from time import time
	
	s0 = time()
	LIGHT_TEST_RESULTS = run_light_test()
	for x in LIGHT_TEST_RESULTS:
		print(x)
	dur1 = time() - s0
	print( "Light Test Duration; ", round(dur1, 2) )

	s1 = time()
	HEAVY_TEST_RESULTS = run_heavy_test()
	for x in LIGHT_TEST_RESULTS:
		print(x)
	dur2 = time() - s1
	print( "Heavy Test Duration;", round(dur2, 2) )
