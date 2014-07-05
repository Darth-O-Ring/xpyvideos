#!/usr/bin/env python2

from distutils.core import setup
from os import remove
from os.path import abspath
from os.path import join as path_join
from os import getcwd
from shutil import copyfile, rmtree
from os import remove
import glob

import xpyvideos


pathname                =               getcwd()

VERSION                 =               '0.0.3-3'

copyfile("xpyvideos.py", "xpyvideos/xpyvideos")

packages                =               ['xpyvideos', 'xpyvideos.packages', 'xpyvideos.packages.pytube']

setup(name              =               'xpyvideos',
      version           =               VERSION,
      description       =               'Python program for downloading videos from xvideos, xhamster, and redtube.',
      author            =               'Darth_O-Ring',
      author_email      =               'darthoring@gmail.com',
      url               =               'https://github.com/Darth-O-Ring/xpyvideos',
      packages          =               packages,
      package_dir       =               {'xpyvideos' : abspath(path_join(pathname, 'xpyvideos/'))},
      scripts           =               ['xpyvideos/xpyvideos'],
      data_files        =               [('share/xpyvideos', ['README.md', 'NOTICE'])],

        )

files       =           ['/usr/bin/opts.py', '/usr/bin/filename.py', '/usr/bin/download.py', '/usr/bin/regexes.py',
                                        '/usr/bin/xpyvideos.py', 'xpyvideos/xpyvideos']
prev_eggs   =       glob.iglob('/usr/lib/python2.7/site-packages/xpyvideos-0.0.*')

for i in xrange(len(files)):
        try:
            if '/usr/bin/' in files[i]:
                remove(abspath(files[i]))

            else:
                remove(abspath(path_join(pathname, files[i])))

        except:
            pass

for i in prev_eggs:
    try:
        temp        =       i.split('/')[-1].split('-')
        
        if temp[1] < VERSION.replace('-', '_'):
            remove(i)

    except:
        pass

try:
    remove('/usr/lib/python2.7/site-packages/xpyvideos-0.0.3_0-py2.7.egg-info')

except:
    pass

try:
    rmtree(abspath(path_join(pathname, 'build/')))

except:
    pass
