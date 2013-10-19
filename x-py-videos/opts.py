# Imports
import argparse
from getpass import getuser



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
