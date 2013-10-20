# Imports
import re
import sys



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

def regex_for_video_link(HTML):
	
	"""
	Uses regular expression to search for flv file link.

	HTML	:	html returned by .read()

	"""

	# Use regular expression to search html for video's url
	reg_ex_for_link		=		re.compile(r'''
									# For xvideos flv link:

									# Don't match beginning of html
							flv_url=	# Start matching once 'flv_url=' is found
							
							(\S+?)		# Group one or more non-whitespace characters 
									# in a non-greedy way so only one link is found
									# This is the video link needed for download
							
							amp		# Stop matching here.  This marks the end of the video link
							
							|		# Mutually exclusive pattern.  Match above or below.

									# For xhamster mp4 link:

							mp4File=	# Start matching at 'mp4File='

							(\S+?)		# Group one or more non-whitespace characters in a
									# non-greedy way so only one link is found
									# This is the video link needed for download.

							"		# Stop matching here.  This marks the end of the video link
							
							|		# Mutually exclusive pattern

									# The same as above but for redtube mp4 link:
							mp4_url=

							(\S+?)

							flv_

							''', re.VERBOSE)

	# Return video link from two item tuple returned by .groups()
	# Handle valid URLs but invalid Xvideo/Xhamster URL errors, causing regex to return a None type, while searching html
	try:

	# Check for where in the tuple the link is
			if reg_ex_for_link.search(HTML).groups()[0] is None and reg_ex_for_link.search(HTML).groups()[1] is None:

	# Return redtube link
				return reg_ex_for_link.search(HTML).groups()[2]

			elif reg_ex_for_link.search(HTML).groups()[0] is None and reg_ex_for_link.search(HTML).groups()[2] is None:

	# Return xhamster link		
				return reg_ex_for_link.search(HTML).groups()[1]
			
			else:

	# Return xvideos link
				return reg_ex_for_link.search(HTML).groups()[0]

	# Catch regex exception
	except (AttributeError, IndexError):
		print """\n\nError: None type returned.\n
				Check that URL is valid: ('http://www.website.com/remaining_link')\n\n"""
		sys.exit(2)


def regex_for_name(HTML):
	"""
	Uses regular expression to search through the html of redtube
		in order to find the video title
		and replace whitespaces with '_'

	HTML	:	html of video link

	"""

	# Compile pattern to look for in HTML
	regex_name		=		re.compile(r'''

							slidePanelMovable">	# Start matching here.  This is where the video title 										      # is.

							\s*			# Match any possible whitespace before the title

							(\D+?)			# Match one or more non digit characters.
										# This is where the video title is.
										# Non-greedy so trailing whitespace doesn't appear

							\s*			# Match any possible whitespace at the end
										# of the video title.

							</h1>			# This is the end of the video titel.
							
							''', re.VERBOSE)

	# Search HTML and substitute whitespace characters
	# Handle possible errors that may occur
	try:
		return ''.join((re.sub(r'\s+', '_', regex_name.search(HTML).groups()[0]), '.mp4'))

	# Catch exceptions when regex returns a None type
	except (AttributeError, IndexError):
		print '\n\nError: Could not find video title in html.\n\n'
		sys.exit(1)
