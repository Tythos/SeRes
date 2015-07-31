""" Tests specific Protocol implementations
"""


import os
import unittest
import sqlite3

import seres.data
from seres.formats import Csv
from seres.protocols import LocalFile, Sqlite
from seres.rest import RestUri
from seres.test.models import get_all_dicts

ru = RestUri("sqlite:///" + seres.data.get_full_path("example.db") + "#flats")

class LocalFileTest(unittest.TestCase):
	def test_local_file(self):
		contents = "This is a test\nThis is only a test"
		rest_path = os.getcwd().replace("\\", "/")
		rest_uri = RestUri("file:///" + rest_path + os.sep + "test.txt")
		lf = LocalFile()
		lf.outbound(rest_uri, contents)
		result = lf.inbound(rest_uri)
		self.assertEquals(result, contents)
	
class SqliteTest(unittest.TestCase):
	def test_table_create(self):
		d = get_all_dicts()
		conn = sqlite3.connect(ru.get_full_path())
		if Sqlite.is_table_exist(conn, ru.frag):
			conn.execute("DROP TABLE " + ru.frag)
		Sqlite.create_table_from_dataset(conn, ru.frag, [d[0]])
		conn.execute("DROP TABLE " + ru.frag)
		conn.commit()
		conn.close()

	def test_table_insert(self):
		s = Sqlite()
		c = Csv()
		d = get_all_dicts()
		text = c.outbound([d[0]])
		s.outbound(ru, text)
		conn = sqlite3.connect(ru.get_full_path())
		results = conn.execute("SELECT * FROM %s" % ru.frag)
		conn.close()

	def test_end_to_end(self):
		d = get_all_dicts()
		c = Csv()
		text = c.outbound([d[0]])
		s = Sqlite()
		s.outbound(ru, text)
		r = s.inbound(ru)

if __name__ == "__main__":
	unittest.main()
