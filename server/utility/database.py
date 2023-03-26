from zlib import compress, decompress
from json import loads as json_loads, dumps as json_dumps
from os import path, makedirs
from typing import Any, Union
from shutil import rmtree


PY_FILE_DIRECTORY = path.dirname(path.realpath(__file__))
VALID_DATABASE_TYPES = Union[dict, list, str, int]

class DatabaseCore:
	filepath = None

	def delete(self) -> None:
		dirpath, _ = path.split(self.filepath)
		if path.exists(dirpath):
			rmtree( dirpath )

	def _write_blank_database(self) -> None:
		try:
			with open(self.filepath, "wb") as file:
				data = compress( "{}".encode() )
				file.write(data)
		except Exception as e:
			print(e)

	def _read_database(self) -> dict:
		if not path.exists(self.filepath):
			self._write_blank_database()
		try:
			with open(self.filepath, "rb") as file:
				data = file.read()
				return json_loads( decompress( data ) )
		except Exception as e:
			print(e)
		return None

	def _write_database(self, database_json : dict) -> bool:
		try:
			data = compress( json_dumps(database_json).encode() )
			with open(self.filepath, "wb") as file:
				file.write( data )
			return True
		except Exception as e:
			print(e)
		return False

	def _dump_decompressed(self, filepath : str) -> None:
		data = json_dumps(self._read_database())
		with open(filepath, "w") as file:
			file.write(data)

	def _set_filepath(self, filepath : str) -> None:
		makedirs( list(path.split(filepath))[0], exist_ok=True )
		self.filepath = filepath

	def __init__(self, filepath=None):
		self._set_filepath(filepath)

class RobloxAnalytics(DatabaseCore):
	place_id = -1

	def _check_datastore_existance( self, database_json : dict, datastore_id : str ) -> dict:
		if database_json == None:
			return None

		# datastore_id datastore
		datastore_id_key = str(datastore_id)
		datastore_database = database_json.get( datastore_id_key )
		if not datastore_database:
			database_json[datastore_id_key] = { }
			datastore_database = database_json[datastore_id_key]

		return datastore_database

	def GetValue( self, datastore_id : str, unique_key : str ) -> Any:
		database = self._read_database()
		datastore = self._check_datastore_existance(database, datastore_id)
		if datastore == None:
			return None
		return datastore.get(unique_key)

	def GetBulkValue( self, datastore_id : str, unique_keys : list[str] ) -> list[Any]:
		database = self._read_database()
		datastore = self._check_datastore_existance(database, datastore_id)
		values = []
		if datastore == None:
			return values
		for key in unique_keys:
			values.append( datastore.get(key) )
		return values

	def SetValue( self, datastore_id : str, unique_key : str, data : VALID_DATABASE_TYPES ) -> None:
		database = self._read_database()
		datastore = self._check_datastore_existance(database, datastore_id)
		if datastore == None:
			return
		datastore[unique_key] = data
		self._write_database(database)

	def SetBulkValue( self, datastore_id : str, unique_keys : list[str], data_values : list[VALID_DATABASE_TYPES] ) -> None:
		database = self._read_database()
		datastore = self._check_datastore_existance(database, datastore_id)
		if datastore == None:
			return
		for unique_key, data in zip( unique_keys, data_values ):
			datastore[unique_key] = data
		self._write_database(database)

	def __init__( self, id="-1" ):
		filepath = path.join( PY_FILE_DIRECTORY, str(id), "data.dat" )
		super().__init__(filepath=filepath)
