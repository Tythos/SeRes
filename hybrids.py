"""Defines hybrid parsers for cases where an intermediary plaintext form is
   counter-productive (i.e., SQL, Excel, etc.) and conversion between
   dictionary lists and the datastore can take place directly.
"""

from seres import parsers
import sqlite3
import sys
import warnings

if sys.version_info.major == 2:
	from urllib import unquote
else:
	from urllib.parse import unquote

class Hybrid(parsers.Parser):
	@classmethod
	def create(cls, ru, dicts):
		"""Creates a new entry in the datastore indicated by the REST URI based
		   on the entries defined in the list of dictionaries
		"""
		raise NotImplementedError("This hybrid parser has an unimplemented CREATE interface")
	
	@classmethod
	def read(cls, ru):
		# Queries a set of entries from the given REST URI
		raise NotImplementedError("This hybrid parser has an unimplemented READ interface")

	@classmethod
	def update(cls, ru, dicts):
		# Pushes a new set of entries (as plaintext) to the given REST URI
		raise NotImplementedError("This hybrid parser has an unimplemented UPDATE interface")

	@classmethod
	def delete(cls, ru):
		# Deletes a set of entries from the given REST URI
		raise NotImplementedError("This hybrid parser has an unimplemented DELETE interface")

class Sqlite(Hybrid):
	@classmethod
	def get_filters(cls):
		f = super(Csv, cls).get_filters()
		f['scheme'] = "^sqlite$"
		return f

	@classmethod
	def create(cls, ru, dicts):
		conn = sqlite3.connect(ru.get_full_path())
		if not Sqlite._is_table_exist(conn, ru.frag):
			Sqlite._create_table_from_dataset(conn, ru.frag, dicts)
		for d in dicts:
			qry = "INSERT INTO %s VALUES (" % ru.frag
			for ndx, field in enumerate(d.keys()):
				if ndx > 0:
					qry += ", "
				qry += Sqlite._get_sql_value_rep(d[field])
			qry += ")"
			conn.execute(qry)
		conn.commit()
		conn.close()
		
	@classmethod
	def read(cls, ru):
		# Specific query arguments are translated into WHERE clauses
		qry = "SELECT * FROM %s" % ru.frag
		for ndx, name in enumerate(ru.query.keys()):
			if ru.query[name] is True:
				this_query = unquote(name)
			else:
				this_query = name + " = " + Sqlite.get_sql_value_rep(ru.query[name])
			if ndx == 0:
				qry += " WHERE " + this_query
			else:
				qry += " AND " + this_query
		conn = sqlite3.connect(ru.get_full_path())
		try:
			results = conn.execute(qry)
		except:
			return []
		columns = results.description
		rows = []
		for row in results:
			this_row = {}
			for ndx, field in enumerate(columns):
				this_row[field[0]] = Sqlite.ptext2value(row[ndx])
			rows.append(this_row)
		conn.close()
		return rows
		
	@classmethod
	def update(cls, ru, dicts):
		if "id" not in dicts[0]:
			warnings.warn("No ID field present; inserting as new entries")
			Sqlite.create(ru, dicts)
		else:
			conn = sqlite3.connect(ru.get_full_path())
			for d in dicts:
				qry = "UPDATE %S SET "
				for ndx, field in enumerate(d.keys()):
					if field != "id":
						if ndx > 0:
							qry += ", "
						qry += "%s = %s" % (field, Sqlite._get_sql_value_rep(d[field]))
				qry += " WHERE id = %u" % d['id']
				conn.execute(qry)
			conn.commit()
			conn.close()
			
	@classmethod
	def delete(cls, ru):
		qry = "DROP TABLE IF EXISTS %s" % ru.frag
		conn = sqlite3.connect(ru.get_full_path())
		conn.execute(qry)
		conn.commit()
		conn.close()
		
	@classmethod
	def _create_table_from_dataset(cls, conn, table_name, dicts):
		qry = "CREATE TABLE %s (" % table_name
		for ndx, field in enumerate(dicts[0].keys()):
			if ndx > 0:
				qry += ", "
			qry += field + " " + Sqlite._get_sqlite_type(dicts, field)
		qry += ")"
		conn.execute(qry)
		conn.commit()
		
	@classmethod
	def _get_sqlite_type(cls, data, field):
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
			
	@classmethod
	def _is_table_exist(cls, conn, table_name):
		return len(conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='" + table_name + "'").fetchmany()) > 0
		
	@classmethod
	def _get_sql_value_rep(cls, value):
		if value is None:
			return "''"
		if type(value) == type(True):
			if value:
				return "'True'"
			else:
				return "'False'"
		elif type(value) is not type(""):
			try:
				f = float(value)
				return str(value)
			except:
				value = str(value)
		return "'%s'" % value.replace("'", "''")
