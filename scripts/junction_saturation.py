#!/usr/bin/env python
'''-------------------------------------------------------------------------------------------------
check detected splicing juntions (and annotated junctions) was saturated or not
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
	parser.add_option("-r","--refgene",action="store",type="string",dest="refgene_bed",help="Reference gene model in bed fomat. This gene model is used to determine known splicing junctions. [required]")
	parser.add_option("-l","--percentile-floor",action="store",type="int",dest="percentile_low_bound",default=5, help="Sampling starts from this percentile. A integer between 0 and 100. default=%default")
	parser.add_option("-u","--percentile-ceiling",action="store",type="int",dest="percentile_up_bound",default=100, help="Sampling ends at this percentile. A integer between 0 and 100. default=%default")
	parser.add_option("-s","--percentile-step",action="store",type="int",dest="percentile_step",default=5, help="Sampling frequency. Smaller value means more sampling times. A integer between 0 and 100. default=%default")	
	parser.add_option("-m","--min-intron",action="store",type="int",dest="minimum_intron_size",default=50, help="Minimum intron size (bp). default=%default")
	parser.add_option("-v","--min-coverage",action="store",type="int",dest="minimum_splice_read",default=1, help="Minimum number of supportting reads to call a junction. default=%default")
	(options,args)=parser.parse_args()

	if not (options.output_prefix and options.input_file and options.refgene_bed):
		parser.print_help()
		sys.exit(0)
	if options.percentile_low_bound <0 or options.percentile_low_bound >100:
		print >>sys.stderr, "percentile_low_bound must be larger than 0 and samller than 100"
		sys.exit(0)
	if options.percentile_up_bound <0 or options.percentile_up_bound >100:
		print >>sys.stderr, "percentile_up_bound must be larger than 0 and samller than 100"
		sys.exit(0)
	if options.percentile_up_bound < options.percentile_low_bound:
		print >>sys.stderr, "percentile_up_bound must be larger than percentile_low_bound"
		sys.exit(0)
	if options.percentile_step <0 or options.percentile_step > options.percentile_up_bound:
		print >>sys.stderr, "percentile_step must be larger than 0 and samller than percentile_up_bound"
		sys.exit(0)
	if os.path.exists(options.input_file) or options.input_file == '-':
		obj = SAM.QCSAM(options.input_file)
		obj.saturation_junction(outfile=options.output_prefix, refgene=options.refgene_bed, sample_start=options.percentile_low_bound,sample_end=options.percentile_up_bound,sample_step=options.percentile_step,min_intron=options.minimum_intron_size,recur=options.minimum_splice_read)
	else:
		print >>sys.stderr, '\n\n' + options.input_file + " does NOT exists" + '\n'
		sys.exit(0)
		#parser.print_help()
		


if __name__ == '__main__':
	main()
