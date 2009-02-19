import ConfigParser, gdata.spreadsheet.service, sys

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

keyfield = config.get( 'parameters', 'keyfield' )
valuefield = config.get( 'parameters', 'valuefield' )

updatemap = dict( [ line.rstrip().split( '\t' ) for line in open( config.get( 'parameters', 'datafile' ) ).readlines() ] )

for entry in gd_client.GetListFeed( key, wksht_id ).entry:
	entrydict = dict( zip( entry.custom.keys(), [ value.text for value in entry.custom.values() ] ) )

	entrykey = entrydict[ keyfield ]
	entryvalue = entrydict[ valuefield ]
	if entrykey in updatemap:
		print "updating row with key {0} from value {1} to {2}".format( entrykey, entrydict[ valuefield ], updatemap[ entrykey ] )
		entrydict[ valuefield ] = updatemap[ entrykey ]
		entry = gd_client.UpdateRow( entry, entrydict )
		del updatemap[ entrykey ]	

if updatemap != {}:
	print "keys not found in document:", ', '.join( updatemap.keys() )