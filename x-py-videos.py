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
VERSION		=		'v0.0.2'


def build_opts():
	"""
	Builds and returns a parser object of command line arguments
	
	"""
	parser		=		argparse.ArgumentParser(description='Xvideos download options.')

	# Add url option
	parser.add_argument('-u', '--url', type=str, required=True, help='url of video to download(Required).',
				metavar='url of video(Required).'
				)

	# Add directory option
	parser.add_argument('-dir', '--directory', type=str, default='/home/{}'.format(getuser()), required=False,
				help='Directory to download video in(Optional).',
				metavar='Directory for video storage(Default=/home/user).'
				)

	# Add filename option
	parser.add_argument('-f', '--filename', type=str, required=False, help='Filename of video desired(Optional).',
				metavar='Filename of video(Default=original video title).'
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


def file_name(arg_f, URL):
	"""
	Assigns and returns a filename.

	arg_f	:	-f/--filename value returned by arg_parser

	URL	:	url of video to be downloaded

	"""
	# Split URL to grab video title if None
	if arg_f == None:
		return URL.split('/')[-1]

	# Otherwise return filename provided with -f/--filename
	else:
		return arg_f


def regex_xvideos(HTML):
	"""
	Uses regular expression to search for flv file link.

	HTML	:	html returned by .read()

	"""

	# Use regular expression to search html for flv url
	reg_ex_for_link		=		re.compile(r'''
									# Don't match beginning of html
							(flv_url=)	# Start matching once ('flv_url=') is found
							
							(\S+)		# Match one or more non-whitespace characters 
									# after ('flv_url=')
									# This is the video link needed for download
							
							(amp)		# Match ('url_').  This marks the end of the video link

								''', re.VERBOSE)

	# Grab video link from three item tuple given by .groups()
	# Handle valid URLs but invalid Xvideo URL errors, causing regex to return a None type, while searching html
	try:
		return reg_ex_for_link.search(HTML).groups()[1]

	# Catch regex exception
	except (AttributeError, IndexError):
		print "\n\nError: None type returned.\nCheck that URL is valid: ('http://www.xvideos.com/remaining_link')\n\n"
		sys.exit(2)


def regex_xhamster(HTML):
	"""
	Uses regular expression to search for mp4 file.

	HTML	:	html returned by .read()

	"""

	# Use regular expression to search html for mp4
	reg_ex_for_link		=		re.compile(r'''
									# Don't match beginning of html
							(mp4File=)	# Start matching once ('mp4File=') is found
							
							(\S+)		# Match one or more non-whitespace characters 
									# after ('mp4File=')
									# This is the video file needed for download
							(")		# Marks end of mp4 file

								''', re.VERBOSE)

	# Grab video link from three item tuple given by .groups()
	# Handle valid URLs but invalid Xhamster URL errors, causing regex to return a None type, while searching html
	try:
		return reg_ex_for_link.search(HTML).groups()[1]

	# Catch regex exception
	except (AttributeError, IndexError):
		print """\n\nError: None type returned.\nCheck that URL is valid: ('http://www.xvideos/ORxhamster.com/remaining_link')
				\n\n"""
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
			print "\nDownloading: {0} (Bytes: {1})\n\n".format(f_name, file_size)
			

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
		print "\n\nError: Failed on: ('{0}').\nCheck that: ('{1}'), is a valid pathname.\n".format(arg_dir, 
													pathname[:-len(f_name)])
		sys.exit(2)
	except BufferError:
		print '\n\nError: Failed on writing buffer.\nFailed to write video to file.\n\n'
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
		print """\n\nError: Check that URL is valid: ('http://www.xvideos/OR_xhamster.com/remaining_link')
				\nFailed on: ('{}')\n\n""".format(url)
		sys.exit(2)
	
	# Call file_name and assign return value to filename variable
	filename		=		file_name(args['f'], url)
	
	# Check for xvideos 
	if 'xvideos.com' in url:
		video_file		=		regex_xvideos(html)
	
	# Add .flv to filename
		filename		=		''.join((filename, '.flv'))

	# Check for xhamster
	elif 'xhamster.com' in url:
		video_file		=		regex_xhamster(html)

	# Replace .html with .mp4 in the case of xhamster
		filename		=		filename.replace('.html', '.mp4')

	# Unquote video file URL
	video_file		=		urllib2.unquote(video_file)

	# Open video file for downloading
	try:
		video_file		=		urllib2.urlopen(video_file)

	
	except (urllib2.URLError, urllib2.HTTPError):
		print "\n\nError: Failed to open video link's URL.\n\n"
		sys.exit(1)
	
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

