from os import path as os_path
from sys import path as sys_path

directory = os_path.abspath(__file__)
sys_path.append( os_path.join(directory, "..", "..") )

from server.tests import database_light, database_heavy, localhost_light, localhost_heavy

def run_light_tests() -> bool:
	results = []

	try:
		results.extend( database_light() )
	except Exception as e:
		print(e)
		return False

	try:
		results.extend( localhost_light() )
	except Exception as e:
		print(e)
		return False
	
	for i, (success, message) in enumerate(results):
		print("Test " + str(i), success and "Succeeded" or "Failed")
		if not success:
			print(message)
			return False

	print("All tests were successful.")
	return True

def run_heavy_tests() -> bool:
	results = []

	try:
		results.extend( database_heavy() )
	except Exception as e:
		print(e)
		return False

	try:
		results.extend( localhost_heavy() )
	except Exception as e:
		print(e)
		return False
	
	for success, message in results:
		if not success:
			print(message)
			return False
	return True

if __name__ == '__main__':
	run_light_tests()

	# print("Setting up analytic server connection.")
	# # STUFF
	# print("Closing analytic server connection.")
