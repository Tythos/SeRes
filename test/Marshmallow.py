from datetime import date
from marshmallow import Schema, fields, pprint

class ArtistSchema(Schema):
    name = fields.Str()

class AlbumSchema(Schema):
    title = fields.Str()
    release_date = fields.Date()
    artist = fields.Nested(ArtistSchema)

def run_demo():
	# OUTPUT SHOULD BE AS FOLLOWS:
	# { 'artist': {'name': 'David Bowie'},
	#   'release_date': '1971-12-17',
	#   'title': 'Hunky Dory'}
	bowie = dict(name='David Bowie')
	album = dict(artist=bowie, title='Hunky Dory', release_date=date(1971, 12, 17))
	schema = AlbumSchema()
	result = schema.dump(album)
	pprint(result.data, indent=2)	
