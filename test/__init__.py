"""Defines the contents and execution interface for seres tests
"""

import importlib
import sys
import types
import unittest

if sys.version_info.major == 2:
	def is_test_case(c):
		return type(c) == types.TypeType and issubclass(c, unittest.TestCase)
else:
	def is_test_case(c):
		return isinstance(c, type) and issubclass(c, unittest.TestCase)

__all__ = [
	"models",
	"protocols",
	"rest",
	"formats",
	"serial"
]

test_dicts = [
	{'one': 1, 'two': 2, 'three': 3},
	{'one': 'uno', 'two': 'dos', 'three': 'tres'},
	{'one': 'ichi', 'two': 'ni', 'three': 'san'}
]

def suite():
	ts = unittest.TestSuite()
	for test_module in __all__:
		m = importlib.import_module("seres.test." + test_module)
		for n in dir(m):
			c = getattr(m, n)
			if is_test_case(c):
				s = unittest.TestLoader().loadTestsFromTestCase(c)
				ts.addTests(s)
	return ts
				
if __name__ == "__main__":
	unittest.TextTestRunner(verbosity=2).run(suite())
