import gdata.spreadsheet.service

import ConfigParser, gdata.spreadsheet.service, sys

if len( sys.argv ) != 2:
	print "list.py list.cfg"
	exit( -1 )

config = ConfigParser.RawConfigParser()
config.read( sys.argv[ 1 ] )

gd_client = gdata.spreadsheet.service.SpreadsheetsService()
gd_client.email = config.get( 'credentials', 'email' )
gd_client.password = config.get( 'credentials', 'password' )
gd_client.source = 'LIST'
gd_client.ProgrammaticLogin()

spreadsheets = gd_client.GetSpreadsheetsFeed()
for sheet in spreadsheets.entry:
	name = sheet.title.text 
	key = sheet.id.text.rsplit('/',1)[-1]
	print name, key
	try:
		worksheets = gd_client.GetWorksheetsFeed( key )
	except gdata.service.RequestError:
		pass
	for ws in worksheets.entry:
		name = ws.title.text
		wksht_id = ws.id.text.rsplit('/',1)[-1]
		print "\t", name , wksht_id
	
