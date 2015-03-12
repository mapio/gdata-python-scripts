## How to configure scipts ##

All the scripts read their configuration from a text file formatted according [RFC 822](http://rfc.net/rfc822.html) and parsed by http://docs.python.org/library/configparser.html.

The sections are: `credentials`, `documentspec` (or `calendarspec`),  and `parameters`, the first one used to authenticate to the service, the second one to pick what spreadsheet and sheet (or calendar) to work on, and the third one for script-specific parameters.

In particular, the `documentspec` section has fields: `key` and `wksht_id` that you can obtain using the `list.py` script of this project. The `calendarspec` has just an `id` field that you can obtain using the `list.py` script of this project, or looking at the Calendar ID field in the "Settings" pane of Google Calendar.

## Spreadsheet scripts ##

### List ###

This script lists `key` and `wksht_id` values for all of your spreadsheets. The only section that needs to be present in the configuration file is `credentials`.

### Dump ###

This script lists the content of a specific sheet of the given spreadsheet. The sections that need to be present in the configuration file are `credentials` and `documentspec`.

### Update ###

This script updates the contents of a specific sheet of the given spreadsheet.

More precisely, given a list of (key, value) pairs (from the `datafile` text file) it will update the rows of the spreadsheet matching the key in the given`keycolumn` and consequently setting the value in the given `valuecolumn`.

For example, assume that the spreadsheet has columns named
```
Name Phone Address
```
and you have a file named `update.txt` containing the following data
```
Ross 555-1234
Brown 555-6789
 ...
```
and that the `parameters` section of the configuration file looks like
```
keycolumn=Name
valuecolumn=Phone
datafile=update.txt
```
then update will change the phone number of Ross to 555-1234, the one of Brown to 555-6789 and so on. leaving other columns unchanged.

## Calendar scripts ##

### List ###

This script lists `id` values for all of your calendars. The only section that needs to be present in the configuration file is `credentials`.

### Dump ###

This script lists the events of a specific calendar. The sections that need to be present in the configuration file are `credentials`, `calendarspec` and `parameters` (that allows to specify a date range, a regexp to filter event titles and other options - please give a look at the configuration file for more information).
