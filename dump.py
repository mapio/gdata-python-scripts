import ConfigParser, gdata.spreadsheet.service, sys

if len( sys.argv ) != 2:
	print "dump.py dump.cfg"
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

for entry in gd_client.GetListFeed( key, wksht_id ).entry:
	entrydict = dict( zip( entry.custom.keys(), [ value.text for value in entry.custom.values() ] ) )
	print entrydict		
