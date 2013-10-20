import sys, os, shutil
from distutils.core import Extension
from setuptools import find_packages, setup

shutil.copyfile("xpyvideos.py", "x-py-videos/xpyvideos.py")

setup(name		=		'x-py-videos',
      version		=		'0.0.2-4',
      description	=		'Python program for downloading videos from xvideos, xhamster, and redtube.',
      author		=		'Darth_O-Ring',
      author_email	=		'darthoring@gmail.com',
      url		=		'https://github.com/Darth-O-Ring/X-Py-Videos',
      packages		=		find_packages(),
      package_dir	=		{'xpyvideos' : 'x-py-videos/'},
      scripts		=		['xpyvideos.py'],
      data_files	=		[('share/xpyvideos', ['README.md', 'NOTICE'])]
	)


