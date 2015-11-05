"""Defines basic parsing behaviors and controllers
"""

from seres import rest

class Parser(object):
	@classmethod
	def get_filters(cls):
		return {}
		
	@classmethod
	def ptext2value(cls, ptext):
		# Parses a plaintext representation of a single value for matching
		# primitive types (True/False, int/float, and defaulting to string)
		if ptext.lower() == "true":
			return True
		elif ptext.lower() == "false":
			return False
		if len(ptext) == 0:
			return None
		try:
			value = int(ptext)
		except:
			try:
				value = float(ptext)
			except:
				value = ptext
		return value

def _get_parser(parsers, ru):
	is_matches = [ru.is_match(f.get_filters()) for f in parsers]
	if True not in is_matches:
		raise Exception("No parser matching the given REST URI was found")
	last_match_ndx = len(is_matches) - is_matches[-1::-1].index(True) - 1
	return parsers[last_match_ndx]
