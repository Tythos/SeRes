""" Defines common Rest utilities, including an extension of the native urlparse class
"""

import os
import sys
if sys.version_info.major == 2:
	from urlparse import urlparse
	from urllib import unquote, quote
else:
	from urllib.parse import urlparse, unquote, quote
from os.path import split as splitpath, splitext
from re import split, match

def _match_all_queries(query):
	return True
	
class RestUri:
	def __init__(self, uri):
		pr = urlparse(uri.replace("\\", "/"))
		self.scheme = pr.scheme if pr.scheme is not None else ""
		self.user = pr.username if pr.username is not None else ""
		self.password = pr.password if pr.password is not None else ""
		self.server = pr.hostname if pr.hostname is not None else ""
		self.port = str(pr.port) if pr.port is not None else ""
		self.dirpath, fullfile = splitpath(pr.path)
		if self.dirpath is None:
			self.dirpath = ""
		self.file, ext = splitext(fullfile)
		if self.file is None:
			self.file = ""
		if len(ext) > 0:
			self.ext = ext[1:]
		else:
			self.ext = ""
		self.query = RestUri.parse_args(pr.query)
		if self.query is None:
			self.query = {}
		self.frag = pr.fragment if pr.fragment is not None else ""
		
	def get_file_name(self):
		return self.file + "." + self.ext
		
	def get_full_path(self):
		full_path = self.dirpath + "/" + self.get_file_name()
		if full_path[0] == "/" and os.sep == "\\":
			# DOS paths should ignore the leading / that indicates a root drive path
			full_path = full_path[1:]
		return full_path
		
	def get_full_uri(self):
		full_uri = self.scheme + "://"
		if len(self.user) > 0:
			full_uri += self.user
			if len(self.password) > 0:
				full_uri += ":" + self.password
			full_uri += "@"
		full_uri += self.server
		if len(self.port) > 0:
			full_uri += ":" + self.port
		full_path = self.get_full_path()
		if os.sep == "\\":
			full_path = "/" + full_path
		full_uri += full_path
		return full_uri
		
	@staticmethod
	def parse_args(query):
		args = {}
		parts = split("&", query)
		for part in parts:
			mSingle = match("^([^=]+)$", part)
			mPair = match("^([\w\d_]+)=(.+)$", part)
			if mSingle is not None:
				args[part] = True
			elif mPair is not None and len(mPair.groups()) == 2:
				g = mPair.groups()
				args[g[0]] = unquote(g[1])
		return args
		
	@staticmethod
	def merge_args(args):
		query = ""
		field_names = args.keys()
		for ndx, f in enumerate(field_names):
			if type(args[f]) == type(True) and args[f]:
				entry = f
			else:
				entry = f + "=" + quote(args[f])
			if ndx > 0:
				query += "&" + entry
			else:
				query = entry
		return query

class RestPattern:
	def __init__(self):
		self.dirpath = ".*"
		self.ext = ".*"
		self.file = ".*"
		self.frag = ".*"
		self.password = ".*"
		self.port = ".*"
		self.query = _match_all_queries
		self.scheme = ".*"
		self.server = ".*"
		self.user = ".*"

	def is_match(self, restUri):
		# Returns true if all patterns match their respective fields
		isMatch = True
		if match(self.dirpath, restUri.dirpath) is None:
			isMatch = False
		if match(self.ext, restUri.ext) is None:
			isMatch = False
		if match(self.file, restUri.file) is None:
			isMatch = False
		if match(self.frag, restUri.frag) is None:
			isMatch = False
		if match(self.password, restUri.password) is None:
			isMatch = False
		if match(self.port, restUri.port) is None:
			isMatch = False
		if match(self.scheme, restUri.scheme) is None:
			isMatch = False
		if match(self.server, restUri.server) is None:
			isMatch = False
		if match(self.user, restUri.user) is None:
			isMatch = False
			
		# Query patterns are matched by specific logic implemented by a user function; by default, this matches everything
		if self.query(restUri.query) is False:
			isMatch = False
		return isMatch
			
		
