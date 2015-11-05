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
import sys
from seres import parsers

if sys.version_info.major == 2:
	from io import BytesIO as StringBuffer
else:
	from io import StringIO as StringBuffer

class Format(parsers.Parser):
	@classmethod
	def ptext2dicts(cls, ptext):
		# Should return a dictionary or collection of dictionaries as parsed
		# from the given plaintext. Dictionary entries should have a uniform
		# schema (though this is less important than for the reverse).
		raise NotImplementedError("This format parser has an unimplemented ptext2dicts interface")

	@classmethod
	def dicts2ptext(cls, dicts):
		# Should return a format-specific representation of the object or
		# collection of objects in plaintext given a list of dictionaries with a
		# uniform schema
		raise NotImplementedError("This format parser has an unimplemented dicts2ptext interface")
		
	@classmethod
	def ptext2value(cls, ptext):
		# Parses a plaintext representation of a single value for matching
		# primitive types (True/False, int/float, and defaulting to string)
		if ptext.lower() == "true":
			return True
		elif ptext.lower() == "false":
			return False
		try:
			value = int(ptext)
		except:
			try:
				value = float(ptext)
			except:
				value = ptext
		return value

class Csv(Format):
	@classmethod
	def get_filters(cls):
		f = super(Csv, cls).get_filters()
		f['ext'] = "^csv$"
		return f

	@classmethod
	def ptext2dicts(cls, ptext):
		header_row = None
		dicts = []
		for row in csv.reader(ptext.splitlines()):
			if header_row is None:
				header_row = row
			else:
				entry = {}
				for ndx, field in enumerate(header_row):
					entry[field] = Format.ptext2value(row[ndx])
				dicts.append(entry)
		return dicts
	
	@classmethod
	def dicts2ptext(cls, dicts):
		field_names = list(dicts[0].keys())
		output = StringBuffer()
		writer = csv.writer(output)
		writer.writerow(field_names)
		for d in dicts:
			writer.writerow(list(d.values()))
		ptext = output.getvalue()
		output.close()
		return ptext
