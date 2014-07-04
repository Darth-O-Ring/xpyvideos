# Imports
from __future__ import print_function
from os.path import abspath, isfile
from os.path import join as path_join
from os import remove
from sys import exit
from urllib2 import urlopen, unquote, URLError, HTTPError
from time import time
from regexes import regex_for_video_link
from filename import file_name


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

def write_video_to_file(arg_dir, vid_file, f_name):
    """
    
    Opens and writes video to file and displays 
        progress bar during download.

    arg_dir     :   -dir/--directory value
    vid_file    :   URL of video file
    f_name      :   filename

    """

    # Open video file for downloading
    # Handle any potential video link errors
    try:
        vid_file    =       urlopen(vid_file)

    # Catch any potential URL errors while opening the video link for download
    except (URLError, HTTPError):
        print("\n\nError: Failed to open video link's URL.\n\n")
        exit(1)

    # Join directory and filename
    pathname        =       abspath(path_join(arg_dir, f_name))

    # Check for conflicting filenames
    if isfile(pathname):
        print("\n\nError: Conflicting filename: ('{}').\nDownload aborted.\n\n".format(f_name))
        exit(1)

    # Grab byte info
    meta            =       vid_file.info()
    file_size       =       int(meta.getheaders("Content-Length")[0])
    file_size_dl    =       0
    block_size      =       8192

    # Open file for writing flv to
    # Handle file opening/writing errors
    try:
        with open(pathname, 'wb') as output:
            print("\nDownloading: '{0}' (Bytes: {1} | Megabytes: {2:.1f})\n\n".format(f_name, file_size, file_size/1024/1024.0))
            start       =       time()

    # Start loop to display progress bar
            while True:

    # Read video files's block size into buffer
                buffer      =       vid_file.read(block_size)

    # Break if empty buffer
                if not buffer:
                    break

    # Add current length of buffer to file's downloaded amount          
                file_size_dl    +=      len(buffer)

    # Write buffer/video's downloaded amount to file
                output.write(buffer)

    # Set download status for display using raw string
                try:
                    status      =       r'{0:10d} Bytes | {1:.1f}MB | Completed: [{2:3.2f}%]    Speed:  {3:.2f} Mb/s'.format(
                                                file_size_dl, 
                                                file_size_dl/1024/1024.0,
                                                file_size_dl * 100.0 / file_size,
                                                float(file_size_dl*8/2**20)/(time()
                                                        - start))
    # Catch error caused in Windows
                except ZeroDivisionError:
                    continue

    # Update status 
                status      =       status + chr(8) * (len(status)+1)

    # Print status to screen
                print(status, end=' ')
    

    # Catch open/write exceptions
    except IOError:
        print("""\n\nError: Failed on: ('{0}').\nCheck that: ('{1}'), is a valid pathname.
            \nOr that ('{2}') is a valid filename.\n\n""".format(arg_dir, pathname[:-len(f_name)], f_name))
        exit(2)

    except BufferError:
        print('\n\nError: Failed on writing buffer.\nFailed to write video to file.\n\n')
        exit(1)

    except KeyboardInterrupt:
        print("\n\nInterrupt signal given.\nDeleting incomplete video ('{}').\n\n".format(f_name))
        remove(pathname)
        exit(1)
    

def download_video(args, url, f_name):
    """

    Grabs necessary html information, searches the html for video's flv url
        and writes it to file.
    
    args    :   dictionary of argument keys/values returned by arg_parser
    url     :   url grabbed from main() for loop
    f_name  :   matching filename to url if -f/--filename was given otherwise it's a list of None

    """

    # Assign url of video
    url         =       url 

    # Open url and grab html information
    # Handle invalid URL errors
    try:
        html        =       urlopen(url).read()

    # Catch URL exceptions
    except (URLError, HTTPError):
        print("\n\nError: Check that URL is valid: ('http://www.website.com/remaining_link')\nFailed on: ('{}')\n\n".format(url))
        exit(2)
    
    # Use regex to search html for the video link
    video_file      =       regex_for_video_link(html)
    
    # Unquote video file URL
    video_file      =       unquote(video_file)

    # Call file_name
    filename        =       file_name(f_name, url, html)
    
    # Call write_video_to_file for video downloading
    write_video_to_file(args['dir'], video_file, filename)

    # Print has finished downloading message
    print("\n\n('{}'): has finished downloading.\n\n".format(filename[:-4]))
