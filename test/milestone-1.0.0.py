"""Test cases demonstrating satisfaction of milestone criteria for v1.0.0
"""

import unittest
import os
from seres import protocols, rest

class TestProtocols(unittest.TestCase):
	def test_file(self):
		# Test the file protocol (file <=> plaintext)
		contents = "This is a test\nThis is only a test"
		rest_path = os.getcwd().replace("\\", "/")
		rest_uri = rest.RestUri("file:///" + rest_path + os.sep + "test.txt")
		lf = protocols.LocalFile()
		lf.outbound(rest_uri, contents)
		result = lf.inbound(rest_uri)
		self.assertEquals(result, contents)
		
if __name__ == "__main__":
	unittest.main()
