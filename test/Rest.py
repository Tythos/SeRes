""" Contains test cases for the SeRes.Rest module
"""

import sys
if sys.version_info.major == 2:
	from urlparse import urlparse
else:
	from urllib.parse import urlparse
from os.path import split
from SeRes.Rest import RestUri, RestPattern


testUri = "https://user:pass@server.org:1234/path/to/file.ext?arg1&arg2=va%3Dl2#frag"


def parseTestOld():
	pr = urlparse(testUri)
	pathParts = split(pr.path)
	toReturn = ""
	toReturn = toReturn + "Test URI: '" + testUri + "':\n"
	toReturn = toReturn + "Required fields:\n"
	toReturn = toReturn + "    PROTOCOL: " + pr.scheme + "' (required)\n"
	toReturn = toReturn + "    FQDN: " + pr.hostname + "' (required)\n"
	toReturn = toReturn + "    PATH: " + pathParts[0] + "' (required)\n"
	toReturn = toReturn + "Optional fields:\n"
	toReturn = toReturn + "    USERNAME: " + pr.username + "\n"
	toReturn = toReturn + "    PASSWORD: " + pr.password + "\n"
	toReturn = toReturn + "    PORT: " + str(pr.port) + "\n"
	toReturn = toReturn + "    FILE: " + pathParts[1] + "\n"
	toReturn = toReturn + "    ARGUMENTS: " + repr(pr.query) + "\n"
	toReturn = toReturn + "    FRAGMENT: " + pr.fragment + "\n"
	return toReturn
	
def parseTest():
	ru = RestUri(testUri)
	assert ru.scheme == "https"
	assert ru.user == "user"
	assert ru.password == "pass"
	assert ru.server == "server.org"
	assert ru.port == "1234"
	assert ru.dirpath == "/path/to"
	assert ru.file == "file"
	assert ru.ext == "ext"
	assert ru.query == {'arg1': True, 'arg2': 'va=l2'}
	assert ru.frag == "frag"

def matchTest():
	ru = RestUri(testUri)
	rp = RestPattern()
	rp.scheme = "^https{0,1}$"
	assert rp.isMatch(ru)
