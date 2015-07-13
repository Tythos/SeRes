""" Defines basic protocol interfaces for providing CRUD operations to/from arbitrary
    data stores. Specific registered Protocol parsers are assigned by matching one or more
	URI components (properties of a RestUri(ParseResult) object)::
	* scheme
	* hostname
	* port
	* path
"""

class Protocol:
	def __init__(self):
		self.pattern.scheme = ""
		self.pattern.hostname = ""
		self.pattern.port = ""
		self.pattern.path = ""

		
class File:
	