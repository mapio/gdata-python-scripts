# gdata-python-scripts, usage examples of Google API Python Client Library
# Copyright (C) 2009 Massimo Santini
#
# This file is part of gdata-python-scripts.
# 
# gdata-python-scripts is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# gdata-python-scripts is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with gdata-python-scripts.  If not, see <http://www.gnu.org/licenses/>.

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

