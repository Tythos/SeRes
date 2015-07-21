"""Defines the contents and execution interface for seres tests
"""

import unittest

__all__ = [
	"Models",
	"protocol",
	"Rest"
]

test_dicts = [
	{'one': 1, 'two': 2, 'three': 3},
	{'one': 'uno', 'two': 'dos', 'three': 'tres'},
	{'one': 'ichi', 'two': 'ni', 'three': 'san'}
]

def run_all():
	for test in __all__:
		#__import__('seres.test.' + test)
		unittest.main(module='seres.test.' + test, exit=False)
	#unittest.main()
	
if __name__ == "__main__":
	run_all()
