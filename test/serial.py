"""test cases for Serial objects and associated behaviors
"""

import unittest
import seres.serial

class SerialTestCase(unittest.TestCase):
	def test_format_detect(self):
		f = seres.serial.get_default_formats()
		
if __name__ == "__main__":
	unittest.main()
