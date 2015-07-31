""" Defines basic protocol interfaces for providing CRUD operations to/from arbitrary
    data stores. Specific registered Protocol parsers are assigned by matching one or more
	URI components (properties of a RestUri(ParseResult) object)::
	* scheme
	* hostname
	* port
	* path
"""

import os
from re import match
import sys
import sqlite3
if sys.version_info.major == 2:
	import urllib2 as urllib
	from urllib import unquote
else:
	import urllib.request as urllib
	from urllib.parse import unquote
from seres.rest import RestPattern
from seres.formats import Csv

class Protocol:
	def __init__(self):
		self.pattern = RestPattern()
	
	def inbound(self, ru):
		raise NotImplementedError("Protocol interface is an abstract class")
	
	def outbound(self, ru, text):
		raise NotImplementedError("Protocol interface is an abstract class")
		
class LocalFile(Protocol):
	def __init__(self):
		Protocol.__init__(self)
		self.pattern.scheme = "^file$"
		self.pattern.server = "^$"
		
	def inbound(self, ru):
		# Inbound method for local file reads file contents and returns as plaintext
		fullpath = ru.dirpath + os.sep + ru.file + "." + ru.ext
		if match("/\w:", fullpath):
			# Local path on Windows drive must truncate leading slash to be passed to open()
			fullpath = fullpath[1:]
		f = open(fullpath, "r")
		contents = f.read()
		f.close()
		return contents
	
	def outbound(self, ru, text):
		# Outbound method for local file writes file contents from plaintext
		fullpath = ru.dirpath + os.sep + ru.file + "." + ru.ext
		if match("/\w:", fullpath):
			# Local path on Windows drive must truncate leading slash to be passed to open()
			fullpath = fullpath[1:]
		f = open(fullpath, "w")
		f.write(text)
		f.close()

class Http(Protocol):
	def __init__(self):
		Protocol.__init__(self)
		self.pattern.scheme = "^https{0,1}$"
		
	def inbound(self, ru):
		response = urllib.urlopen(ru.get_full_uri())
		return response.read()
	
	def outbound(self, ru, text):
		raise Exception("HTTP protocol is read-only")

class Sqlite(Protocol):
	def __init__(self):
		Protocol.__init__(self)
		self.pattern.scheme = "^sqlite$"
		
	def inbound(self, ru):
		# Inbound sqlite commands inerpret a REST URI into the following basic SELECT query:
		#	SELECT * FROM [fragment] WHERE [query]
		# The args in [query[ can be standard "[field]=[value]", or encoded
		# versions of more advanced comparisons (i.e., "age > 10", etc.)
		# More sophisticated query operations, such as chained and embedded
		# queries, must be implemented either by multiple REST-ful requests
		# or by filtering/sorting data once it has been queried and deserialized
		# into the appropriate arrangement.
		#
		# The resulting table is returned as a CSV-style plaintext table. The
		# easiest way to do this is actually to transcribe the result table into
		# an intermediate dictionary, then use the format.Csv object for
		# the transcription to plaintext for access by other formats.
		query = "SELECT * FROM %s" % ru.frag
		for ndx, name in enumerate(ru.query.keys()):
			if ru.query[name] is True:
				this_query = unquote(name)
			else:
				this_query = name + " = " + Sqlite.get_sql_value_rep(ru.query[name])
			if ndx == 0:
				query += " WHERE " + this_query
			else:
				query += " AND " + this_query
		conn = sqlite3.connect(ru.get_full_path())
		results = conn.execute(query)
		columns = results.description
		rows = []
		for row in results:
			this_row = {}
			for ndx, field in enumerate(columns):
				this_row[field[0]] = row[ndx]
			rows.append(this_row)
		c = Csv()
		conn.close()
		return c.outbound(rows)
	
	def outbound(self, ru, text):
		# Does one of two actions, depending on the existence of the table indicated by @[fragment]
		# * If the table exists, attempts a basic series of INSERT commands
		# * If the table does not exist, attempts CREATE , followed by INSERT, where CREATE field types
		#   are determined from commonality
		# Note that any query arguments are ignored.
		conn = sqlite3.connect(ru.get_full_path())
		c = Csv()
		data = c.inbound(text)
		if not Sqlite.is_table_exist(conn, ru.frag):
			Sqlite.create_table_from_dataset(conn, ru.frag, data)
		for datum in data:
			qry = "INSERT INTO %s VALUES (" % ru.frag
			for ndx, field in enumerate(datum.keys()):
				if ndx > 0:
					qry += ","
				qry += Sqlite.get_sql_value_rep(datum[field])
			qry += ")"
			conn.execute(qry)
		conn.commit()
		conn.close()
		
	@staticmethod
	def create_table_from_dataset(conn, table_name, data):
		qry = "CREATE TABLE %s (" % table_name
		for ndx, field in enumerate(data[0].keys()):
			if ndx > 0:
				qry += ", "
			qry += field + " " + Sqlite.get_sqlite_type(data, field)
		qry += ")"
		conn.execute(qry)
		conn.commit()
		
	@staticmethod
	def get_sqlite_type(data, field):
		is_numeric = True
		for d in data:
			if type(d[field]) is not type(""):
				try:
					f = float(d[field])
				except:
					is_numeric = False
			else:
				is_numeric = False
		if is_numeric:
			return "real"
		else:
			return "text"
		
	@staticmethod
	def is_table_exist(conn, table_name):
		return len(conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='" + table_name + "'").fetchmany()) > 0
		
	@staticmethod
	def get_sql_value_rep(value):
		# Converts an arbitrary string, numeric, or logical value into a format
		# that can be referenced inside an SQL query
		if type(value) == type(True):
			if value:
				return "1"
			else:
				return "0"
		elif type(value) == type(""):
			return "'" + value + "'"
		else:
			return value
