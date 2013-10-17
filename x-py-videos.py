#!/usr/bin/python2

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

# Imports
import urllib2
import argparse
import sys
import re
import os
from getpass import getuser

# Version number
VERSION		=		'v0.0.2-3'


def build_opts():
	"""
	Builds and returns a parser object of command line arguments
	
	"""
	parser		=		argparse.ArgumentParser(description='X-Py-Videos command line options.')

	# Add url option
	parser.add_argument('-u', '--url', type=str, required=True, help='url of video to download(Required).',
				metavar=''
				)

	# Add directory option
	parser.add_argument('-dir', '--directory', type=str, default='/home/{}'.format(getuser()), required=False,
				help='Directory to download video in(Optional).', metavar=''
				)

	# Add filename option
	parser.add_argument('-f', '--filename', type=str, required=False, help='Filename of video desired(Optional).',
				metavar=''
				)

	# Return parser
	return parser


def arg_parser(parser):
	"""
	Parses command line arguments and returns a dictionary
		of argument values

	Parser	:	object containing valid command line options

	"""
	
	# Parse arguments
	args		=		parser.parse_args()

	# Build and return dictionary
	return {	'u'	:	args.url
		,	'dir'	:	args.directory
		,	'f'	:	args.filename if '-f' or '--filename' in args else None
		}


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


def write_video_to_file(arg_dir, vid_file, f_name):
	"""
	
	Opens and writes video to file and displays 
		progress bar during download.

	vid_file	:	open video file
	f_name		:	filename
	arg_dir		:	-dir/--directory value

	"""

	# Join directory and filename
	pathname		=		os.path.abspath(os.path.join(arg_dir, f_name))

	# Grab byte info
	meta			=		vid_file.info()
	file_size		=		int(meta.getheaders("Content-Length")[0])
	file_size_dl		=		0
	block_size		=		8192

	# Open file for writing flv to
	# Handle file opening/writing errors
	try:
		with open(pathname, 'wb') as output:
			print "\nDownloading: '{0}' (Bytes: {1})\n\n".format(f_name, file_size)
			

	# Start loop to display progress bar
			while True:

	# Read video files's block size into buffer
				buffer		=		vid_file.read(block_size)

	# Break if empty buffer
				if not buffer:
					break

	# Add current length of buffer to file's downloaded amount			
				file_size_dl	+=		len(buffer)

	# Write buffer/video's downloaded amount to file
				output.write(buffer)

	# Set download status for display using raw string
				status		=		r'{:10d} [{:3.2f}%]'.format(file_size_dl, 
												file_size_dl * 100.0 / file_size)

	# Update status 
				status		=		status + chr(8) * (len(status)+1)

	# Print status to screen
				print status,

	# Catch open/write exceptions
	except IOError:
		print """\n\nError: Failed on: ('{0}').\nCheck that: ('{1}'), is a valid pathname.\n
				Or that ('{2}') is a valid filename.\n\n""".format(arg_dir, pathname[:-len(f_name)], f_name)
		sys.exit(2)

	except BufferError:
		print '\n\nError: Failed on writing buffer.\nFailed to write video to file.\n\n'
		sys.exit(1)

	except KeyboardInterrupt:
		print "\n\nInterrupt signal given.\nDeleting incomplete video ('{}').\n\n".format(f_name)
		os.remove(pathname)
		sys.exit(1)


def download_video(args):
	"""

	Grabs necessary html information, searches the html for video's flv url
		and writes it to file.
	
	args	:	dictionary of argument keys/values returned by arg_parser

	"""

	# Assign url of video
	url			=		args['u']

	# Open url and grab html information
	# Handle invalid URL errors
	try:
		html			=		urllib2.urlopen(url).read()

	# Catch URL exceptions
	except (urllib2.URLError, urllib2.HTTPError):
		print """\n\nError: Check that URL is valid: ('http://www.website.com/remaining_link')
				\nFailed on: ('{}')\n\n""".format(url)
		sys.exit(2)
	
	# Use regex to search html for the video link
	video_file		=		regex_for_video_link(html)
	
	# Unquote video file URL
	video_file		=		urllib2.unquote(video_file)

	# Open video file for downloading
	# Handle any potential video link errors
	try:
		video_file		=		urllib2.urlopen(video_file)

	# Catch any potential URL errors while opening the video link for download
	except (urllib2.URLError, urllib2.HTTPError):
		print "\n\nError: Failed to open video link's URL.\n\n"
		sys.exit(1)
	
	# Call file_name
	filename		=		file_name(args['f'], url, html)
	
	# Call write_video_to_file for video downloading
	write_video_to_file(args['dir'], video_file, filename) 

	# Print has finished downloading message
	print "\n\n('{}'): has finished downloading.\n\n".format(filename[:-4])


def main():
	"""
	main()

	Parse command line arguments and calls download 
		for downloading video.

	"""

	# Handle command line options
	args		=		arg_parser(build_opts())

	# Call download_video
	download_video(args)


if __name__	==	'__main__':
	# Display program name/author info 
	print '\nX-Py-Videos {0} by: {1} Running...\n'.format(VERSION, __Author__)

	main()

