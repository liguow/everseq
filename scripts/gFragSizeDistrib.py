#!/usr/bin/env python
'''-------------------------------------------------------------------------------------------------
Calculate the fragment size (determined from genomic location) of RNA-seq experiemnt. 
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
__version__="1.0.6"
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
	parser.add_option("-o","--out-prefix",action="store",type="string",dest="output_prefix",help="Prefix of output files(s). [required]")
	parser.add_option("-l","--lower-bound",action="store",type="int",dest="lower_bound_size",default=0,help="Lower bound of fragmental size (bp). This option is used for ploting histograme. default=%default")
	parser.add_option("-u","--upper-bound",action="store",type="int",dest="upper_bound_size",default=500,help="Upper bound of fragmental size (bp). This option is used for plotting histogram. default=%default")
	parser.add_option("-s","--step",action="store",type="int",dest="step_size",default=5,help="Step size (bp) of histograme. This option is used for plotting histogram. default=%default")	
	(options,args)=parser.parse_args()

	if not (options.output_prefix and options.input_file):
		parser.print_help()
		sys.exit(0)
	for input_file in ([options.input_file]):
		if input_file == "-":
			continue
		if not os.path.exists(input_file):
			print >>sys.stderr, '\n\n' + input_file + " does NOT exists" + '\n'
			parser.print_help()
			sys.exit(0)
	if options.step_size <=0:
		print >>sys.stderr, "step size is a positive interger"
		sys.exit(0)
	obj = SAM.QCSAM(options.input_file)
	obj.genomicFragSize(outfile=options.output_prefix,low_bound=options.lower_bound_size,up_bound=options.upper_bound_size,step=options.step_size)


if __name__ == '__main__':
	main()
