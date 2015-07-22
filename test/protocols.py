""" Tests specific Protocol implementations
"""


import os
import unittest

from seres.protocols import LocalFile
from seres.rest import RestUri

class LocalFileTest(unittest.TestCase):
	def test_local_file(self):
		contents = "This is a test\nThis is only a test"
		rest_path = os.getcwd().replace("\\", "/")
		rest_uri = RestUri("file:///" + rest_path + os.sep + "test.txt")
		lf = LocalFile()
		lf.outbound(rest_uri, contents)
		result = lf.inbound(rest_uri)
		self.assertEquals(result, contents)
	