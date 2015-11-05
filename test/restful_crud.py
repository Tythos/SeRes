"""Defines use-cases for verifying requirements and providing examples
"""

import unittest
import seres
from seres import test

objs = test.get_all_models()

class FileCsv(unittest.TestCase):
	def test_create(self):
		seres.create("file:///C:/Users/Brian/Projects/seres/test/test.csv", objs)
		
	def test_read(self):
		objs = seres.read("file:///C:/Users/Brian/Projects/seres/test/test.csv")
		
	def test_update(self):
		seres.read("file:///C:/Users/Brian/Projects/seres/test/test.csv", objs)

	def test_delete(self):
		seres.delete("file:///C:/Users/Brian/Projects/seres/test/test.csv")

if __name__ == "__main__":
	unittest.main()
	