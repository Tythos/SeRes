""" Defines basic protocol interfaces for providing CRUD operations to/from arbitrary
    data stores. Specific registered Protocol parsers are assigned by matching one or more
	URI components (properties of a RestUri(ParseResult) object)::
	* scheme
	* hostname
	* port
	* path
"""

import os
from re import match
import sys
if sys.version_info.major == 2:
	import urllib2 as urllib
else:
	import urllib.request as urllib
from seres.rest import RestPattern


class Protocol:
	def __init__(self):
		self.pattern = RestPattern()
	
	def inbound(self, ru):
		raise NotImplementedError("Protocol interface is an abstract class")
	
	def outbound(self, ru, text):
		raise NotImplementedError("Protocol interface is an abstract class")

		
class LocalFile(Protocol):
	def __init__(self):
		Protocol.__init__(self)
		self.pattern.scheme = "^file$"
		self.pattern.server = "^$"
		
	def inbound(self, ru):
		# Inbound method for local file reads file contents and returns as plaintext
		fullpath = ru.dirpath + os.sep + ru.file + "." + ru.ext
		if match("/\w:", fullpath):
			# Local path on Windows drive must truncate leading slash to be passed to open()
			fullpath = fullpath[1:]
		f = open(fullpath, "r")
		contents = f.read()
		f.close()
		return contents
	
	def outbound(self, ru, text):
		# Outbound method for local file writes file contents from plaintext
		fullpath = ru.dirpath + os.sep + ru.file + "." + ru.ext
		if match("/\w:", fullpath):
			# Local path on Windows drive must truncate leading slash to be passed to open()
			fullpath = fullpath[1:]
		f = open(fullpath, "w")
		f.write(text)
		f.close()

class Http(Protocol):
	def __init__(self):
		Protocol.__init__(self)
		self.pattern.scheme = "^https{0,1}$"
		
	def inbound(self, ru):
		response = urllib.urlopen(ru.get_full_uri())
		return response.read()
	
	def outbound(self, ru):
		raise Exception("HTTP protocol is read-only")