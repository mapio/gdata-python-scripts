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
