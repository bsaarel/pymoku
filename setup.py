import subprocess, os, os.path, sys

from setuptools import setup, Extension

from pkg_resources import resource_filename, resource_isdir
from tempfile import mkstemp
from zipfile import ZipFile
from glob import glob

version = open('pymoku/version.txt').read().strip()

# I thought this fixed a bug on Windows but I'm now not convinved, should
# check that this is required (rather than just using '/' as path sep.)
j = os.path.join

lr_ext = Extension(
	'lr',
	include_dirs=['liquidreader'],
	sources=glob('liquidreader/*.c') + glob('lr_mod/*.c'),
	extra_compile_args=['-std=c99'],
)

setup(
	name='pymoku',
	version=version,
	author='Ben Nizette',
	author_email='ben.nizette@liquidinstruments.com',
	packages=['pymoku', 'pymoku.tools'],
	package_dir={'pymoku': 'pymoku'},
	package_data={
		'pymoku' : ['version.txt', '*.capnp', j('data', '*')]
	},
	license='MIT',
	long_description="Python scripting interface to the Liquid Instruments Moku:Lab",

	url="https://github.com/liquidinstruments/pymoku",
	download_url="https://github.com/liquidinstruments/pymoku/archive/%s.tar.gz" % version,

	keywords=['moku', 'liquid instruments', 'test', 'measurement', 'lab', 'equipment'],

	entry_points={
		'console_scripts' : [
			'moku=pymoku.tools.moku:main',
			'moku_convert=pymoku.tools.moku_convert:main',
		]
	},

	install_requires=[
		'future',
		'pyzmq>=15.3.0',
		'six',
		'urllib3',
		'pyzmq',
		'rfc6266',
		'requests',
		'decorator',
	],

	ext_modules=[
		lr_ext,
	],

	zip_safe=False, # Due to bitstream download
)
