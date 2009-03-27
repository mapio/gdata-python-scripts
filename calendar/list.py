import ConfigParser
import sys

import gdata.calendar.service

if len( sys.argv ) != 2:
	print "callist.py callist.cfg"
	exit( -1 )

config = ConfigParser.RawConfigParser()
config.read( sys.argv[ 1 ] )

gd_client = gdata.calendar.service.CalendarService()
gd_client.email = config.get( 'credentials', 'email' )
gd_client.password = config.get( 'credentials', 'password' )
gd_client.source = 'DUMP'
gd_client.ProgrammaticLogin()

feed = gd_client.GetAllCalendarsFeed()

print 'Calendars of %s' % feed.title.text

for cal in feed.entry:
	print cal.title.text, 
	for link in cal.link:
		if link.rel == 'edit': print link.href.split( '/' )[ -1 ].replace( '%40', '@' )
