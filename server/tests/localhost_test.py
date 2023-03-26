from requests import get as requests_get, post as requests_post
from os import path as os_path
from sys import path as sys_path
from json import dumps as json_dumps
from hashlib import md5

directory = os_path.abspath(__file__)
sys_path.append( os_path.join(directory, "..", "..", "..") )

from server.utility.server import SetupLocalHost, ServerThreadWrapper
# from server.utility.certificate import GenerateDefaultCertificateBase64

LATEST : str = ""

def run_light_test() -> list[ (bool, str) ]:
	TEST_RESULTS = []
	
	def CallbackExample(self, content_length : int, content : str) -> int:
		global LATEST
		LATEST = content
		return 200

	host : ServerThreadWrapper = SetupLocalHost(port=9999, onGET=CallbackExample, onPOST=CallbackExample)

	sample_data_1 = json_dumps({"test" : 1})
	requests_get("http://localhost:9999", data=sample_data_1)
	if sample_data_1 == LATEST:
		TEST_RESULTS.append((True, "GET data has successfully been sent over localhost."))
	else:
		TEST_RESULTS.append((False, "GET data has unsuccessfully been sent over localhost."))

	sample_data_2 = json_dumps({"test" : 2})
	requests_post("http://localhost:9999", data=sample_data_2)
	if sample_data_2 == LATEST:
		TEST_RESULTS.append((True, "POST data has successfully been sent over localhost."))
	else:
		TEST_RESULTS.append((False, "POST data has unsuccessfully been sent over localhost."))

	host.shutdown()
	return TEST_RESULTS

def run_heavy_test() -> list[ (bool, str) ]:
	return []

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
	for x in HEAVY_TEST_RESULTS:
		print(x)
	dur2 = time() - s1
	print( "Heavy Test Duration;", round(dur2, 2) )
