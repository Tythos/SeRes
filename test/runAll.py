""" Run all package tests (eventually)
"""

from SeRes.test.Models import Flat, Child, DataStructures
from SeRes.test.Rest import parseTest, matchTest


def reportTest(f):
	try:
		f()
	except:
		print(f.__name__ + " FAILED")
	else:
		print(f.__name__ + " PASSED")	
	
def modelTest():
	f = Flat()
	c = Child()
	ds = DataStructures()
	f.saySomething()
	c.getSignature()
	repr(ds)

def runAll():
	reportTest(modelTest)
	reportTest(parseTest)
	reportTest(matchTest)

	
if __name__ == "__main__":
	runAll()
