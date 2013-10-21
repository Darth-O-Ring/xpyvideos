#!/usr/bin/env python2

import shutil
from setuptools import setup, find_packages

shutil.copyfile("xpyvideos.py", "xpyvideos/xpyvideos")

setup(name		=		'xpyvideos',
      version		=		'0.0.2-4',
      description	=		'Python program for downloading videos from xvideos, xhamster, and redtube.',
      author		=		'Darth_O-Ring',
      author_email	=		'darthoring@gmail.com',
      url		=		'https://github.com/Darth-O-Ring/X-Py-Videos',
      packages		=		find_packages(),
      scripts		=		['xpyvideos.py'],
      data_files	=		[('share/xpyvideos', ['README.md', 'NOTICE'])]
	)


