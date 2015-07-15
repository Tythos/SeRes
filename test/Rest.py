""" Contains test cases for the SeRes.Rest module
"""

import sys
if sys.version_info.major == 2:
	from urlparse import urlparse
else:
	from urllib.parse import urlparse
from os.path import split
from seres.rest import RestUri, RestPattern


test_uri = "https://user:pass@server.org:1234/path/to/file.ext?arg1&arg2=va%3Dl2#frag"


def urlparse_test():
	pr = urlparse(test_uri)
	path_parts = split(pr.path)
	to_return = ""
	to_return = to_return + "Test URI: '" + test_uri + "':\n"
	to_return = to_return + "Required fields:\n"
	to_return = to_return + "    PROTOCOL: " + pr.scheme + "' (required)\n"
	to_return = to_return + "    FQDN: " + pr.hostname + "' (required)\n"
	to_return = to_return + "    PATH: " + path_parts[0] + "' (required)\n"
	to_return = to_return + "Optional fields:\n"
	to_return = to_return + "    USERNAME: " + pr.username + "\n"
	to_return = to_return + "    PASSWORD: " + pr.password + "\n"
	to_return = to_return + "    PORT: " + str(pr.port) + "\n"
	to_return = to_return + "    FILE: " + path_parts[1] + "\n"
	to_return = to_return + "    ARGUMENTS: " + repr(pr.query) + "\n"
	to_return = to_return + "    FRAGMENT: " + pr.fragment + "\n"
	return to_return
	
def parse_test():
	ru = RestUri(test_uri)
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

def match_test():
	ru = RestUri(test_uri)
	rp = RestPattern()
	rp.scheme = "^https{0,1}$"
	assert rp.is_match(ru)
