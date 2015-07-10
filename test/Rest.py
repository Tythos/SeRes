""" Contains test cases for the SeRes.Rest module
"""

from urlparse import urlparse
from os.path import split


testUri = "https://user:pass@server.org:1234/path/to/file.ext?arg1&arg2=val2#frag"


def parseTest():
	pr = urlparse(testUri)
	pathParts = split(pr.path)
	toReturn = ""
	toReturn = toReturn + "Test URI: '" + testUri + "':"
	toReturn = toReturn + "Required fields:"
	toReturn = toReturn + " PROTOCOL: " + pr.scheme + "' (required)"
	toReturn = toReturn + "     FQDN: " + pr.hostname + "' (required)"
	toReturn = toReturn + "     PATH: " + pathParts[0] + "' (required)"
	toReturn = toReturn + "Optional fields:"
	toReturn = toReturn + "    USERNAME: " + pr.username
	toReturn = toReturn + "    PASSWORD: " + pr.password
	toReturn = toReturn + "    PORT: " + str(pr.port)
	toReturn = toReturn + "    FILE: " + pathParts[1]
	toReturn = toReturn + "    ARGUMENTS: " + repr(pr.query)
	toReturn = toReturn + "    FRAGMENT: " + pr.fragment
	return toReturn
	

if __name__ == "__main__":
	parseTest()
