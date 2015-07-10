""" Run all package tests (eventually)
"""

from Models import Flat, Child, DataStructures
from Rest import parseTest

def modelTest():
	f = Flat()
	c = Child()
	ds = DataStructures()
	f.saySomething()
	c.getSignature()
	repr(ds)

def runAll():
	try:
		modelTest()
	except:
		print "modelTest FAILED"
	else:
		print "modelTest PASSED"

	try:
		parseTest()
	except:
		print "parseTest FAILED"
	else:
		print "parseTest PASSED"

		
if __name__ == "__main__":
	runAll()
