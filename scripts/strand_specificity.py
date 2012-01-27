#!/usr/bin/env python
'''-------------------------------------------------------------------------------------------------
strand-specificity is measured by comparing the mapped reads to the expected transcribed strand 
based on annotation. For non-splice reads, real strand are determined from parental gene, while
for splice reads, real strand are determined from splicing motif like GT/AG
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
__version__="1.0.5"
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
	parser.add_option("-r","--refgene",action="store",type="string",dest="ref_gene_model",help="Reference gene model in bed format. This file is better to be a pooled gene model as it will be used to annotate splicing junctions [required]")
	parser.add_option("-g","--genome",action="store",type="string",dest="raw_genome", help="Raw genome sequence in fasta format [required]")
	parser.add_option("-m","--motif",action="store",type="string",dest="motif", default="GTAG,GCAG,ATAC", help="splicing motif. default=%default [optional]")
	parser.add_option("-o","--out-prefix",action="store",type="string",dest="output_prefix",help="Prefix of output files(s). [required]")
	(options,args)=parser.parse_args()
		
	if not (options.output_prefix and options.input_file and options.ref_gene_model and options.raw_genome):
		parser.print_help()
		sys.exit(0)
	if not os.path.exists(options.ref_gene_model):
		print >>sys.stderr, '\n\n' + options.ref_gene_model + " does NOT exists" + '\n'
		sys.exit(0)
	if not os.path.exists(options.raw_genome):
		print >>sys.stderr, '\n\n' + options.ref_gene_model + " does NOT exists" + '\n'
		sys.exit(0)
	if os.path.exists(options.input_file) or options.input_file == '-':
		obj = SAM.QCSAM(options.input_file)
		obj.strand_specificity(outfile=options.output_prefix,refbed=options.ref_gene_model,genome=options.raw_genome,sp=options.motif)
	else:
		print >>sys.stderr, '\n\n' + options.input_file + " does NOT exists" + '\n'
		sys.exit(0)			


if __name__ == '__main__':
        main()
