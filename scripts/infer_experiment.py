#!/usr/bin/env python
'''-------------------------------------------------------------------------------------------------
Infer RNA-seq experiment design from SAM/BAM file. This module will determine if the RNA-seq
experiment is:
1) pair-end or single-end
2) strand-specific or not. 
3) if experiment is strand-specific, how reads were stranded.
	* For pair-end RNA-seq, there are two configurations:
		** 1++,1--,2+-,2-+
			*** read1 mapped to '+' strand indicates parental gene on '+' strand
			*** read1 mapped to '-' strand indicates parental gene on '-' strand
			*** read2 mapped to '+' strand indicates parental gene on '-' strand
			*** read2 mapped to '-' strand indicates parental gene on '+' strand
		** 1+-,1-+,2++,2--
			*** read1 mapped to '+' strand indicates parental gene on '-' strand
			*** read1 mapped to '-' strand indicates parental gene on '+' strand
			*** read2 mapped to '+' strand indicates parental gene on '+' strand
			*** read2 mapped to '-' strand indicates parental gene on '-' strand
	* For single-end RNA-seq, there are two configurations:
		** ++,--
			*** read mapped to '+' strand indicates parental gene on '+' strand
			*** read mapped to '-' strand indicates parental gene on '-' strand
		** +-,-+
			*** read mapped to '+' strand indicates parental gene on '-' strand
			*** read mapped to '-' strand indicates parental gene on '+' strand		
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
	parser.add_option("-i","--input-file",action="store",type="string",dest="input_file",help="Input file in SAM format. Use \"-\" represents standard input[required]")
	parser.add_option("-r","--refgene",action="store",type="string",dest="refgene_bed",help="Reference gene model in bed fomat. [required]")
	parser.add_option("-s","--sample_size",action="store",type="int",dest="sample_size",default=200000, help="Number of reads sampled from SAM/BAM file. default=%default")	
	(options,args)=parser.parse_args()

	if not (options.input_file and options.refgene_bed):
		parser.print_help()
		sys.exit(0)
	if os.path.exists(options.input_file) or options.input_file == '-':
		obj = SAM.QCSAM(options.input_file)
		obj.configure_experiment(refbed=options.refgene_bed, sample_size = options.sample_size)
	else:
		print >>sys.stderr, '\n\n' + options.input_file + " does NOT exists" + '\n'
		#parser.print_help()
		sys.exit(0)
		


if __name__ == '__main__':
	main()
