"""test cases for Serial objects and associated behaviors
"""

import unittest
import os
from seres.rest import RestUri
import seres.serial
from seres.test.models import get_all_models, get_all_dicts

class FilterTestCase(unittest.TestCase):
	def test_format_detect(self):
		f = seres.serial.get_default_formats()
		names = []
		for fi in f:
			names.append(fi.__class__.__name__)
		self.assertEqual(names, ['Csv', 'Json'])
	
	def test_protocol_detect(self):
		p = seres.serial.get_default_protocols()
		names = []
		for pi in p:
			names.append(pi.__class__.__name__)
		self.assertEqual(names, ['Http', 'LocalFile'])
		
class SerialDeserialTestCase(unittest.TestCase):
	def test_serial(self):
		f, c, ds = get_all_models()
		s = seres.serial.Serial()
		r = s.serialize([f, c, ds])
		self.assertEqual(r, [
			{'__uni__': 'seres.test.models.Flat', 'numeric': 1.62, 'logical': True, 'name': '[unknown]'},
			{'__uni__': 'seres.test.models.Child', 'title': 'Class Instance Extraordinaire', 'numeric': 1.62, 'logical': True, 'name': '[unknown]'},
			{'__uni__': 'seres.test.models.DataStructures', 'array': [False, 2, 'three'], 'dict': {'three': {'field': 'value', 'empty': {}}, 'two': 2, 'one': True}}
		])
		
	def test_deserial(self):
		d = get_all_dicts()
		s = seres.serial.Serial()
		r = s.deserialize(d)

class CsvPipeline(unittest.TestCase):
	def test_outbound(self):
		s = seres.serial.Serial()
		f, c, ds = get_all_models()
		test_file_path = os.path.dirname(os.path.realpath(__file__))
		s.outbound(RestUri("file:///" + test_file_path + os.sep + "test.csv"), [f, c, ds])
		
if __name__ == "__main__":
	unittest.main()
