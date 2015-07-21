"""Test cases for various Format implementations
"""

import unittest
import seres.formats
from seres.test import test_dicts

class CsvTestCase(unittest.TestCase):
	def test_basic_dicts(self):
		cs = seres.formats.CsvFormat()
		plaintext = cs.outbound(test_dicts)
		dicts = cs.inbound(plaintext)
		
if __name__ == "__main__":
	unittest.main()