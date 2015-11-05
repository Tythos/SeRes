"""Defines basic parsing behaviors and controllers
"""

from seres import rest

class Parser(object):
	@classmethod
	def get_filters(cls):
		return {}
		
def _get_parser(parsers, ru):
	is_matches = [ru.is_match(f.get_filters()) for f in parsers]
	if True not in is_matches:
		raise Exception("No parser matching the given REST URI was found")
	last_match_ndx = len(is_matches) - is_matches[-1::-1].index(True) - 1
	return parsers[last_match_ndx]
