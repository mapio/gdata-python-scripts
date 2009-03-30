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