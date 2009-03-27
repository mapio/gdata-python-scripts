import ConfigParser
import re
import sys

import dateutil.parser as date_parser

import gdata.calendar.service

if len( sys.argv ) != 2:
	print "caldump.py caldump.cfg"
	exit( -1 )

defaults = { 
	'max_results' : sys.maxint, 
	'orderby' : 'starttime',
	'sortorder' : 'ascending',
	'ctz' : 'Europe/Rome',
	'time_format' : '%c',
}

config = ConfigParser.RawConfigParser( defaults )
config.read( sys.argv[ 1 ] )

gd_client = gdata.calendar.service.CalendarService()
gd_client.email = config.get( 'credentials', 'email' )
gd_client.password = config.get( 'credentials', 'password' )
gd_client.source = 'DUMP'
gd_client.ProgrammaticLogin()

calendar = config.get( 'calendarspec', 'id' )
filter = re.compile( config.get( 'parameters', 'title' ) )
time_format = config.get( 'parameters', 'time_format' )

query = gdata.calendar.service.CalendarEventQuery( calendar )

query.start_min = config.get( 'parameters', 'start' )
query.start_max =  config.get( 'parameters', 'end' )

query.max_results = config.getint( 'parameters', 'max_results' )
query.orderby = config.get( 'parameters', 'orderby' )
query.sortorder = config.get( 'parameters', 'sortorder' )
query.ctz = config.get( 'parameters', 'ctz' )

feed = gd_client.CalendarQuery( query )

print 'Events of %s' % feed.title.text

for event in feed.entry:
	title = event.title.text
	if filter.match( title ):
		date = date_parser.parse( event.when[0].start_time ).strftime( time_format )
		content = event.content.text
		print date, title
		print "---"
		print content
		print "---\n"

