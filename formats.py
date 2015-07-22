"""Defines abstract Format interface and basic format-specific parsers

Format objects are responsible for parsing a dictionary or set of dictionaries
to and from plaintext. Because this does not include specific CRUD operations
against a specific data resource, only inbound/outbound operations are performed.
The appropriate Format parser is determined by the first registered entry with a
matching .pattern property, and specific instances of Format parsers are registered
by an instance of the Serial class, which handles a quasi-global context.

For now, "dicts" inputs and outputs are assumed to have a uniform schema. Eventually,
logic will need to be added to merge all fields when parsing/generating sets of dictionaries
(though it may be more appropriate to enforce this in Serial).
"""

import csv
import json
import sys
if sys.version_info.major == 2:
	from io import BytesIO as StringBuffer
else:
	from io import StringIO as StringBuffer
from seres.rest import RestPattern

class Format:
	def __init__(self):
		self.pattern = RestPattern()

	def inbound(self, plaintext):
		# Should return a dictionary or collection of dictionaries as parsed from the given plaintext
		raise NotImplementedError("Format interface is a quasi-abstract class")
		
	def outbound(self, dicts):
		# Should return a format-specific representation of the object or collection of objects in plaintext
		raise NotImplementedError("Format interface is a quasi-abstract class")

class Csv(Format):
	def __init__(self):
		Format.__init__(self)
		self.pattern.ext = "^csv$"
		
	def inbound(self, plaintext):
		header_row = None
		dicts = []
		for row in csv.reader(plaintext.split()):
			if header_row is None:
				header_row = row
			else:
				entry = {}
				for ndx, field in enumerate(header_row):
					entry[field] = row[ndx]
				dicts.append(entry)
		return dicts
	
	def outbound(self, dicts):
		field_names = list(dicts[0].keys())
		output = StringBuffer()
		writer = csv.writer(output)
		writer.writerow(field_names)
		for d in dicts:
			writer.writerow(list(d.values()))
		return output.getvalue()
		
class Json(Format):
	def __init__(self):
		Format.__init__(self)
		self.pattern.ext = "^json$"
		
	def inbound(self, plaintext):
		return json.loads(plaintext)
	
	def outbound(self, dicts):
		return json.dumps(dicts)
