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
import sqlite3
from seres import parsers

if sys.version_info.major == 2:
	import urllib2 as urllib
	from urllib import unquote
else:
	import urllib.request as urllib
	from urllib.parse import unquote

class Protocol(parsers.Parser):
	@classmethod
	def create(cls, ru, ptext):
		# Pushes a new set of entries (as plaintext) to the given REST URI
		raise NotImplementedError("This protocol parser has an unimplemented CREATE interface")
	
	@classmethod
	def read(cls, ru):
		# Queries a set of entries from the given REST URI
		raise NotImplementedError("This protocol parser has an unimplemented READ interface")

	@classmethod
	def update(cls, ru, ptext):
		# Pushes a new set of entries (as plaintext) to the given REST URI
		raise NotImplementedError("This protocol parser has an unimplemented UPDATE interface")

	@classmethod
	def delete(cls, ru):
		# Deletes a set of entries from the given REST URI
		raise NotImplementedError("This protocol parser has an unimplemented DELETE interface")
		
class LocalFile(Protocol):
	@classmethod
	def get_filters(cls):
		f = super(LocalFile, cls).get_filters()
		f['scheme'] = "^file$"
		return f

	@classmethod
	def create(cls, ru, ptext):
		with open(ru.get_full_path(), "w") as f:
			f.write(ptext)
	
	@classmethod
	def read(cls, ru):
		with open(ru.get_full_path(), "r") as f:
			content = f.read()
		return content

	@classmethod
	def update(cls, ru, ptext):
		with open(ru.get_full_path(), "w") as f:
			f.write(ptext)

	@classmethod
	def delete(cls, ru):
		os.remove(ru.get_full_path())
