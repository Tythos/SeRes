"""test cases for Serial objects and associated behaviors
"""

import unittest
import seres.serial

class SerialTestCase(unittest.TestCase):
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
		
if __name__ == "__main__":
	unittest.main()
