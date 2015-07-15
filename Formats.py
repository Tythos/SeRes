""" Defines abstract Format interface and basic format-specific parsers

    Format objects are responsible for parsing a dictionary or set of dictionaries
	to and from plaintext. Because this does not include specific CRUD operations
	against a specific data resource, only inbound/outbound operations are performed.
	The appropriate Format parser is determined by the first registered entry with a
	matching .pattern property, and specific instances of Format parsers are registered
	by an instance of the Serial class, which handles a quasi-global context.
"""

from seres.rest import RestPattern

class Format:
	def __init__(self):
		self.pattern = RestPattern()
		raise NotImplementedError("Format interface is an abstract class")

	def inbound(self, plaintext):
		# Should return a dictionary or collection of dictionaries as parsed from the given plaintext
		raise NotImplementedError("Format interface is an abstract class")
		
	def outbound(self, obj):
		# Should return a format-specific representation of the object or collection of objects in plaintext
		raise NotImplementedError("Format interface is an abstract class")
