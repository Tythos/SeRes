""" Defines models that are serialized and deserialized by test routines
"""

import unittest
from seres.serial import Serial

class Flat:
	def __init__(self):
		self.logical = True
		self.numeric = 1.62
		self.name = "[unknown]"
	
	def say_something(self):
		return '"' + self.name + '" is somewhere around ' + str(self.numeric) + '? ' + str(self.logical) + '!'
		
class Child(Flat):
	def __init__(self):
		Flat.__init__(self)
		self.title = "Class Instance Extraordinaire"
		
	def get_signature(self):
		return self.name + ', ' + self.title
		
class DataStructures:
	def __init__(self):
		self.array = [False, 2, "three"]
		self.dict = {'one': True, 'two': 2, 'three': {'field': 'value', 'empty': {}}}
	
	def __repr__(self):
		return "array: " + repr(self.array) + "; dictionary: " + repr(self.dict)

class ModelsTestCase(unittest.TestCase):
	def test_basic_models(self):
		f, c, ds = get_all_models()
		
def get_all_models():
	f = Flat()
	c = Child()
	ds = DataStructures()
	return f, c, ds

def get_all_dicts():
	f, c, ds = get_all_models()
	s = Serial()
	return s.serialize([f, c, ds])
	
if __name__ == "__main__":
	f, c, ds = get_all_models()
	print(f)
	print(c)
	print(ds)
