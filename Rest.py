""" Defines common Rest utilities, including an extension of the native urlparse class
"""

import sys
if sys.version_info.major == 2:
	from urlparse import urlparse
	from urllib import unquote
else:
	from urllib.parse import urlparse, unquote		
from os.path import split as splitpath, splitext
from re import split, match


def _matchAllQueries(query):
	return True
	

class RestUri:
	def __init__(self, uri):
		pr = urlparse(uri)
		self.scheme = pr.scheme
		self.user = pr.username
		self.password = pr.password
		self.server = pr.hostname
		self.port = str(pr.port)
		self.dirpath, fullfile = splitpath(pr.path)
		self.file, ext = splitext(fullfile)
		if len(ext) > 0:
			self.ext = ext[1:]
		else:
			self.ext = ""
		self.query = RestUri.parseArgs(pr.query)
		self.frag = pr.fragment
		
	def getFileName(self):
		return self.file + self.ext
		
	@staticmethod
	def parseArgs(query):
		args = {}
		parts = split("&", query)
		for part in parts:
			mSingle = match("^([\w\d_]+)$", part)
			mPair = match("^([\w\d_]+)=(.+)$", part)
			if mSingle is not None:
				args[part] = True
			elif mPair is not None and len(mPair.groups()) == 2:
				g = mPair.groups()
				args[g[0]] = unquote(g[1])
		return args

class RestPattern:
	def __init__(self):
		self.dirpath = ".*"
		self.ext = ".*"
		self.file = ".*"
		self.frag = ".*"
		self.password = ".*"
		self.port = ".*"
		self.query = _matchAllQueries
		self.scheme = ".*"
		self.server = ".*"
		self.user = ".*"

	def isMatch(self, restUri):
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
			
		