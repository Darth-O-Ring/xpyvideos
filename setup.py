import sys, os, shutil
from distutils.core import setup, Extension
from setuptools import find_packages

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



print "Cleaning up..."
try:
	removeall("build/")
    	os.rmdir("build/")
except:
	pass

try:
	os.remove("x-py-videos/xpyvideos")
except:
	 pass

def capture(cmd):
	return os.popen(cmd).read().strip()

def removeall(path):
	if not os.path.isdir(path):
		return

	files=os.listdir(path)

	for x in files:
		fullpath=os.path.join(path, x)
		if os.path.isfile(fullpath):
			f=os.remove		
			rmgeneric(fullpath, f)
		elif os.path.isdir(fullpath):
			removeall(fullpath)
			f=os.rmdir
			rmgeneric(fullpath, f)
																
def rmgeneric(path, __func__):
	try:
		__func__(path)													
	except OSError, (errno, strerror):
		pass
