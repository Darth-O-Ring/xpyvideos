# Imports
from regexes import regex_for_name


# Author and licensing
__Author__ = "Darth_O-Ring"
__Email__ = "darthoring@gmail.com"
__License__ = """
Copyright (C) 2013-2015  Darth_O-Ring	<darthoring@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

def file_name(arg_f, URL, HTML):
	"""
	Assigns and returns a filename.

	arg_f	:	-f/--filename value returned by arg_parser

	URL	:	url of video to be downloaded

	HTML	:	html to search in the case of redtube for video title

	"""

	# Split URL to grab video title if None and from xhamster with .mp4
	if arg_f is None and 'xhamster.com' in URL:
		return ''.join((URL.split('/')[-1][:-5], '.mp4'))

	# Split URL to grab video title if None and from xvideos with .flv
	elif arg_f is None and 'xvideos.com' in URL:
		return ''.join((URL.split('/')[-1], '.flv'))
	
	# Check for redtube and return a filename from the video title if -f/--filename is None
	elif arg_f is None and 'redtube.com' in URL:
		return regex_for_name(HTML)

	# Check for xvideos and return filename provided with .flv
	elif arg_f is not None and 'xvideos.com' in URL:
		return ''.join((arg_f, '.flv'))

	# Check for redtube and return filename provided
	elif arg_f is not None and 'redtube.com' in URL:
		return ''.join((arg_f, '.mp4'))

	# Otherwise it's xhamster and return filename provided with .mp4
	else:
		return ''.join((arg_f, '.mp4'))
