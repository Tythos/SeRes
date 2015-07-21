"""Serial objects are responsible for:
* Maintaining specific catalogues of Format and Protocol parsers
* Serializing and deserializing Python objects to and from dictionary equivalents

Eventually, the second item will need to support more complex types, such as
user-defined enumerations. For now, the following field values are supported in the basic
release:
* Three primitives
    * Logicals
    * Numerics
    * Strings
* Two data structures
    * Dictionaries
	* Lists
	
Serial objects also define the method by which specific inbound/outbound operations are
mapped to specific Format and Protocol parsers, usually by matching REST URI patterns.
Therefore, the Serial instance is the primary user interface to the seres inobund/outbound
data pipeline.
"""

import types
import seres.formats
import seres.protocols

class Serial():
	def __init__(self):
		self.formats = []
		self.protocols = []
		
	def inbound(self, dictionaries):
		raise NotImplementedError("TODO")
	
	def outbound(self, objects):
		raise NotImplementedError("TODO")	
		
def get_default_formats():
	# Iterate through the contents of seres.formats to initialize and return default
	# instantiations of all Format objects
	formats = []
	for f in dir(seres.formats):
		c = getattr(seres.formats, f)
		if type(c) == types.ClassType:
			if issubclass(c, seres.formats.Format) and c is not getattr(seres.formats, 'Format'):
				formats.append(c())
	return formats

if __name__ == "__main__":
	raise Exception("No command-line interface is currently implemented")
