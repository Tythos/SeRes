"""Test cases for various Format implementations
"""

import unittest
import seres.formats
from seres.test import test_dicts
from seres.test.models import get_all_dicts

class CsvTestCase(unittest.TestCase):
	def test_basic_dicts(self):
		cs = seres.formats.Csv()
		plaintext = cs.outbound(test_dicts)
		dicts = cs.inbound(plaintext)
		
	def test_seres_dicts(self):
		cs = seres.formats.Csv()
		d0 = get_all_dicts()
		pt = cs.outbound(d0)
		df = cs.inbound(pt)
		
class JsonTestCase(unittest.TestCase):
	def test_basic_dicts(self):
		j = seres.formats.Json()
		plaintext = j.outbound(test_dicts)
		dicts = j.inbound(plaintext)
		
	def test_seres_dicts(self):
		j = seres.formats.Json()
		d0 = get_all_dicts()
		pt = j.outbound(d0)
		df = j.inbound(pt)

class PickleTestCase(unittest.TestCase):
	def test_basic_dicts(self):
		p = seres.formats.Pickle()
		plaintext = p.outbound(test_dicts)
		dicts = p.inbound(plaintext)

	def test_seres_dicts(self):
		p = seres.formats.Pickle()
		d0 = get_all_dicts()
		pt = p.outbound(d0)
		df = p.inbound(pt)

if __name__ == "__main__":
	unittest.main()