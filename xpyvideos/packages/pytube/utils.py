from __future__ import print_function
import re
from time import time



def safe_filename(text, max_length=200):
    """
    Sanitizes filenames for many operating systems.

    Keyword arguments:
    text -- The unsanitized pending filename.
    """
    #Quickly truncates long filenames.
    truncate = lambda text: text[:max_length].rsplit(' ', 0)[0]

    #Tidy up ugly formatted filenames.
    text = text.replace('_', ' ')
    text = text.replace(':', ' -')

    #NTFS forbids filenames containing characters in range 0-31 (0x00-0x1F)
    ntfs = [chr(i) for i in range(0, 31)]

    #Removing these SHOULD make most filename safe for a wide range
    #of operating systems.
    paranoid = ['\"', '\#', '\$', '\%', '\'', '\*', '\,', '\.', '\/', '\:',
                '\;', '\<', '\>', '\?', '\\', '\^', '\|', '\~', '\\\\']

    blacklist = re.compile('|'.join(ntfs + paranoid), re.UNICODE)
    filename = blacklist.sub('', text)
    return truncate(filename)


def print_status(progress, file_size, megabytes, start_time):
    """
    This function - when passed as `on_progress` to `Video.download` - prints
    out the current download progress.

    Arguments:
    progress -- The lenght of the currently downloaded bytes.
    file_size -- The total size of the video.
    """

    percent = progress * 100. / file_size
    status = r"{0:10d}  Bytes | {1:.1f} MB | Completed: [{2:3.2f}%]     Speed:   {3:.2f} Mb/s".format(progress, progress/1024/1024.0, percent,
                                                                                float(progress*8/2**20)/(time() - start_time))
    status = status + chr(8) * (len(status) + 1)
    print(status, end=' ')
