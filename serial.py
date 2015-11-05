"""Serial objects are responsible for:
* Maintaining specific catalogues of Format and Protocol parsers
* Serializing and deserializing Python objects to and from dictionary equivalents

Eventually, the second item will need to support more complex types, such as
user-defined enumerations. For now, the following field values are supported in the basic
release:
* Three primitives
    * Logicals
    * Numerics
    * Strings
* Two data structures
    * Dictionaries
	* Lists
	
Serial objects also define the method by which specific inbound/outbound operations are
mapped to specific Format and Protocol parsers, usually by matching REST URI patterns.
Therefore, the Serial instance is the primary user interface to the seres inobund/outbound
data pipeline.
"""

import importlib
import types
import sys
import warnings
import seres.formats
import seres.protocols
import seres.rest
from seres import parsers

if sys.version_info.major == 2:
	def is_class_type(c):
		return type(c) == types.ClassType
else:
	def is_class_type(c):
		return isinstance(c, type)

def dicts2objs(dicts):
	# Populate instantiations of each object using the __uni__ property to
	# determine (and import, if necessary) the appropriate module
	objs = []
	for dict in dicts:
		try:
			module_name, class_name = dict['__uni__'].rsplit(".", 1)
			if module_name not in sys.modules:
				m = importlib.import_module(module_name)
			else:
				m = sys.modules[module_name]
			c = getattr(m, class_name)
			obj = c()
			for field in list(dict.keys()):
				if field != "__uni__":
					setattr(obj, field, dict[field])
			objs.append(obj)
		except Exception as e:
			# In reality, there will be a large number of different things
			# that could go wrong; we should chain try-except, or implement
			# our own exceptions for the deserialization process.
			warnings.warn("Unable to deserialize to class at UNI '" + dict['__uni__'] + "'; a None will be inserted instead", RuntimeWarning)
			objs.append(None)
	return objs
	
def objs2dicts(objs):
	# Convert list of objects into a list of dicts
	dicts = []
	for obj in objs:
		dict = obj.__dict__
		dict['__uni__'] = obj.__module__ + "." + obj.__class__.__name__
		dicts.append(dict)
	return get_tabular_dicts(dicts)

def get_tabular_dicts(dicts):
	# Given an array of dictionary representations of serialized objects, returns a
	# similar array with indentical fields for each entry that will be empty when
	# irrelevant (None values are used for empty fields). Fields are also re-ordered
	# for consistent organization between objects. This is particularly useful for
	# outbound methods of tabular formats, which only have one header row for all entries.
	all_fields = []
	for d in dicts:
		for k in d.keys():
			if k not in all_fields:
				all_fields.append(k)
	all_fields.sort()
	tdicts = []
	for d in dicts:
		nd = {}
		for f in all_fields:
			if f in d:
				nd[f] = d[f]
			else:
				nd[f] = None
		tdicts.append(nd)
	return tdicts
