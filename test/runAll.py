""" Run all package tests (eventually)
"""

from Models import getAll

def runAll():
	f, c, ds = getAll()
	f.saySomething()
	print c.getSignature()
	print repr(ds)

if __name__ == "__main__":
	runAll()
