#!/usr/bin/env python
'''-------------------------------------------------------------------------------------------------
Calculating Phred Quality Score for each position on read. Note that each read should have 
the fixed (same) length
-------------------------------------------------------------------------------------------------'''

#import built-in modules
import os,sys
import re
import string
from optparse import OptionParser
import warnings
import string
import collections
import math
import sets
from time import strftime

#import third-party modules
from bx.bitset import *
from bx.bitset_builders import *
from bx.intervals import *

#import my own modules
from qcmodule import SAM
#changes to the paths

#changing history to this module


__author__ = "Liguo Wang"
__copyright__ = "Copyright 2010, Wei Li's Lab"
__credits__ = []
__license__ = "GPL"
<<<<<<< HEAD
__version__="1.0.6"
=======
__version__="1.0.5"
>>>>>>> 7142d30483fae4447bc4d8822a6f31cd3673182c
__maintainer__ = "Liguo Wang"
__email__ = "liguow@bcm.edu"
__status__ = "Development" #Prototype or Production


def printlog (mesg):
	'''print progress into stderr and log file'''
	mesg="@ " + strftime("%Y-%m-%d %H:%M:%S") + ": " + mesg
	LOG=open('class.log','a')
	print >>sys.stderr,mesg
	print >>LOG,mesg


def main():
	usage="%prog [options]" + '\n' + __doc__ + "\n"
	parser = OptionParser(usage,version="%prog " + __version__)
	parser.add_option("-i","--input-file",action="store",type="string",dest="input_file",help="Input file in SAM format. Use \"-\" represents standard input [required]")
	parser.add_option("-l","--read-len",action="store",type="int",dest="read_length",help="Length of read. Note that read's length need to be fixed. [required]")
	parser.add_option("-o","--out-prefix",action="store",type="string",dest="output_prefix",help="Prefix of output files(s). [required]")
	(options,args)=parser.parse_args()

	if not (options.output_prefix and options.input_file and options.read_length):
		parser.print_help()
		sys.exit(0)
	if os.path.exists(options.input_file) or options.input_file == '-':
		obj = SAM.ParseSAM(options.input_file)
		obj.qualSAM(outfile=options.output_prefix, read_len = options.read_length)
	else:
		print >>sys.stderr, '\n\n' + options.input_file + " does NOT exists" + '\n'
		#parser.print_help()
		sys.exit(0)




if __name__ == '__main__':
	main()
