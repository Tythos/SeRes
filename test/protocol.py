""" Tests specific Protocol implementations
"""


from seres.protocols import LocalFile
from seres.rest import RestUri
import os


def local_file_test():
	contents = "This is a test\nThis is only a test"
	rest_path = os.getcwd().replace("\\", "/")
	rest_uri = RestUri("file:///" + rest_path + os.sep + "test.txt")
	lf = LocalFile()
	lf.outbound(rest_uri, contents)
	result = lf.inbound(rest_uri)
	assert result == contents
	