#!/usr/bin/env python2

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
from download import *
from opts import *

# Version number
VERSION		=		'v0.0.2-4'


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

