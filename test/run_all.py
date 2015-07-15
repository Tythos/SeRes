""" Run all package tests (eventually)
"""

from seres.test.models import Flat, Child, DataStructures
from seres.test.rest import parse_test, match_test
from seres.test.protocol import local_file_test

def report_test(f):
	try:
		f()
	except:
		print(f.__name__ + " FAILED")
	else:
		print(f.__name__ + " PASSED")	
	
def model_test():
	f = Flat()
	c = Child()
	ds = DataStructures()
	f.say_something()
	c.get_signature()
	repr(ds)

def run_all():
	report_test(model_test)
	report_test(parse_test)
	report_test(match_test)
	report_test(local_file_test)

	
if __name__ == "__main__":
	run_all()
