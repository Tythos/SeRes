"""Defines the main entry point / interface for external users. Specific
   mechanisms and routings required to execute the full spectrum of Seres
   inbound and outbound data processes are hidden within a basic CRUD interface.
   See use case documentation and test cases for more details and examples.
"""

from seres import rest, formats, protocols, serial, parsers

allFormats = [formats.Csv]
allProtocols = [protocols.LocalFile]

def _get_pipeline(uriStr):
	ru = rest.RestUri(uriStr)
	format = parsers._get_parser(allFormats, ru)
	protocol = parsers._get_parser(allProtocols, ru)
	return ru, format, protocol
	
def create(uriStr, objs):
	ru, format, protocol = _get_pipeline(uriStr)
	dicts = serial.objs2dicts(objs)
	ptext = format.dicts2ptext(dicts)
	protocol.create(ru, ptext)

def read(uriStr):
	ru, format, protocol = _get_pipeline(uriStr)
	ptext = protocol.read(ru)
	dicts = format.ptext2dicts(ptext)
	return serial.dicts2objs(dicts)
	
def update(uriStr, objs):
	ru, format, protocol = _get_pipeline(uriStr)
	dicts = serial.objs2dicts(objs)
	ptext = format.dicts2ptext(dicts)
	protocol.update(ru, ptext)
	
def delete(uriStr, objs):
	ru, format, protocol = _get_pipeline(uriStr)
	dicts = serial.objs2dicts(objs)
	ptext = format.dicts2ptext(dicts)
	protocol.delete(ru)
