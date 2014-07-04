#!/usr/bin/env python2

# Imports
from __future__ import print_function
import argparse
from os import getcwd
from xpyvideos.download import *
from xpyvideos.youpy import *
from sys import exit


# Author and licensing
__Author__ = "Darth_O-Ring"
__Email__ = "darthoring@gmail.com"
__License__ = """
Copyright (C) 2013-2015  Darth_O-Ring   <darthoring@gmail.com>

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

# Version number
VERSION     =       'v0.0.3-1'


def build_opts():
    """
    Builds and returns a parser object of command line arguments
    
    """
    parser      =       argparse.ArgumentParser(description='X-Py-Videos command line options.')

    # Add url option
    parser.add_argument('url', type=str,
                help='url of video to download(Required).\nIf using multiple urls use a comma delimiter.  Ex: <link1,link2,link3>',
                metavar=''
                )

    # Add directory option
    parser.add_argument('-dir', '--directory', type=str, default=getcwd(), required=False,
                help='Directory to download video in(Optional).', metavar=''
                )

    # Add filename option
    parser.add_argument('-f', '--filename', type=str, nargs='+', default=None, required=False,
                help='Filename of video desired(Optional).\nIf using multiple names use a comma delimiter.  Ex: <name1,name2,name3>',
                metavar=''
                )

    # Adding conversion option
    parser.add_argument('-c', action="store_true", default=False, required=False,
                help='Video to mp3 conversion using ffmpeg(Optional).'
                )

    # Add delete original option
    parser.add_argument('-do', action="store_true", default=False, required=False,
                help='Deletes original video copy if -c and -do is given(Optional).'
                )

    # Return parser
    return parser


def arg_parser(parser):
    """
    Parses command line arguments and returns a dictionary
        of argument values

    Parser  :   object containing valid command line options

    """
    
    # Parse arguments
    args        =       parser.parse_args()

    # Build and return dictionary
    return {'u'     :   args.url.split(',')
            ,'dir'  :   args.directory
            ,'f'    :   args.filename if args.filename is not None else [args.filename]
            ,'c'    :   args.c
            ,'do'   :   args.do
            }

def main():
    """
    main()

    Parse command line arguments and calls download 
        for downloading video.

    """

    # Handle command line options
    args            =       arg_parser(build_opts())

    # Check for unequal ratio of links to filenames
    # Appending None to filenames list if more links are given
    if len(args['u']) > len(args['f']):
        for i in xrange(len(args['u']) - len(args['f'])):
            args['f'].append(None)

    # Print error message if more filenames are given than there are links
    # and exit
    elif len(args['f']) > len(args['u']):
        print("\nError: Unequal ration between URLs and filenames.\nMore filenames given than URLs.\n")
        exit(2)
  
    # Loop through url list and
    # Check if downloading from youtube
    for i in xrange(len(args['u'])):
        if 'youtube.com' in args['u'][i]:
            download_youtube(args, args['u'][i], args['f'][i])   
    
    # Otherwise it's either xvideos, xhamster, or redtube
        else:
            download_video(args, args['u'][i], args['f'][i])


if __name__ ==  '__main__':
    # Display program name/author info 
    print('\nX-Py-Videos {0} by: {1} Running...\n'.format(VERSION, __Author__))

    # Call main()
    main()

    print('\n')
