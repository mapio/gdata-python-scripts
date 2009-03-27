import ConfigParser
import sys

import gdata.spreadsheet.service


if len( sys.argv ) != 2:
	print "update.py update.cfg"
	exit( -1 )

config = ConfigParser.RawConfigParser()
config.read( sys.argv[ 1 ] )

gd_client = gdata.spreadsheet.service.SpreadsheetsService()
gd_client.email = config.get( 'credentials', 'email' )
gd_client.password = config.get( 'credentials', 'password' )
gd_client.source = 'UPDATE'
gd_client.ProgrammaticLogin()

key = config.get( 'documentspec', 'key' )
wksht_id = config.get( 'documentspec', 'wksht_id' )

keycolumn = config.get( 'parameters', 'keycolumn' )
valuecolumn = config.get( 'parameters', 'valuecolumn' )

updatemap = dict( [ line.rstrip().split( '\t' ) for line in open( config.get( 'parameters', 'datafile' ) ).readlines() ] )

for entry in gd_client.GetListFeed( key, wksht_id ).entry:
	entrydict = dict( zip( entry.custom.keys(), [ value.text for value in entry.custom.values() ] ) )

	entrykey = entrydict[ keycolumn ]
	entryvalue = entrydict[ valuecolumn ]
	if entrykey in updatemap:
		print "updating row with key {0} from value {1} to {2}".format( entrykey, entrydict[ valuecolumn ], updatemap[ entrykey ] )
		entrydict[ valuecolumn ] = updatemap[ entrykey ]
		entry = gd_client.UpdateRow( entry, entrydict )
		del updatemap[ entrykey ]	

if updatemap != {}:
	print "keys not found in document:", ', '.join( updatemap.keys() )