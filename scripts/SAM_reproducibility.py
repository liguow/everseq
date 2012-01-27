#!/usr/bin/env python
'''-------------------------------------------------------------------------------------------------
Check the reproducibility of two RNA-seq experiments. Must provide two SAM files. A MA-plot and 
another RPKM scatter plot will be generated
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
	parser.add_option("-a","--file1",action="store",type="string",dest="sam_file_1",help="Input file in SAM format. [required]")
	parser.add_option("-b","--file2",action="store",type="string",dest="sam_file_2",help="Input file in SAM format. [required]")
	parser.add_option("-r","--refgene",action="store",type="string",dest="ref_gene_model",help="Reference gene model in bed format. [required]")
	parser.add_option("-o","--out-prefix",action="store",type="string",dest="output_prefix",help="Prefix of output files(s). [required]")
	parser.add_option("-c","--pseudo-count",action="store",type="float",dest="pseudo_count",default=0.001,help="Prefix of output files(s). default=%default")
	(options,args)=parser.parse_args()

	if not (options.output_prefix and options.sam_file_1 and options.sam_file_2 and options.ref_gene_model):
		parser.print_help()
		sys.exit(0)
	for input_file in ([options.sam_file_1,options.sam_file_2,options.ref_gene_model]):
		if not os.path.exists(input_file):
			print >>sys.stderr, '\n\n' + input_file + " does NOT exists" + '\n'
			#parser.print_help()
			sys.exit(0)

	obj = SAM.QCSAM(options.sam_file_1)
	rpkm1 = obj.mRNA_RPKM(refbed=options.ref_gene_model)
	obj = SAM.QCSAM(options.sam_file_2)
	rpkm2 = obj.mRNA_RPKM(refbed=options.ref_gene_model)
	
	
	RS = open(options.output_prefix + ".RPKM.cor.r",'w')
	print >>RS, 'png("RPKM_coorelation.png",width=800,height=800,pointsize=14)'
	print >>RS, 'rpkm_1=c(' + ','.join([str(rpkm1[i]) for i in sorted(rpkm1.iterkeys())]) + ')'
 	print >>RS, 'rpkm_2=c(' + ','.join([str(rpkm2[i]) for i in sorted(rpkm2.iterkeys())]) + ')'
 	print >>RS, 'pv=cor(rpkm_1,rpkm_2)'
 	print >>RS, 'ym=max(log10(rpkm_2 + %f))' % options.pseudo_count
 	print >>RS, 'xn=min(log10(rpkm_1 + %f))' % options.pseudo_count
 	print >>RS, 'plot(log10(rpkm_1 + %f),log10(rpkm_2 + %f), xlab="%s PRKM (log10)",ylab="%s RPKM (log10)",pch=4,cex=0.4,col="blue", main="")' % (options.pseudo_count,options.pseudo_count,os.path.basename(options.sam_file_1), os.path.basename(options.sam_file_2))
	print >>RS, 'text(x=c(xn, xn + 0.2), y=c(ym-0.5,ym-0.5),labels=c("r = ",pv),adj=0)'
	print >>RS, 'abline(a=0,b=1,col="red",lty="dashed")'
	print >>RS, 'dev.off()' + '\n'
	#print >>RS, 'pcor=cor.test(log10(rpk
	
	print >>RS, 'png("RPKM_MA.png",width=800,height=800,pointsize=14)'
	print >>RS, 'fold = (rpkm_1 + %f)/(rpkm_2 + %f)' % (options.pseudo_count,options.pseudo_count)
	print >>RS, 'avg = ((rpkm_1 + %f) + (rpkm_2 + %f))/2' % (options.pseudo_count,options.pseudo_count)
	print >>RS, 'plot(log2(avg),log2(fold),xlab="Average RPKM (log2)",ylab="Fold Change (log2)",main="MA plot",col="blue",pch=4,cex=0.8,ylim=c(-5,5),xlim=c(-5,15))'
	print >>RS, 'abline(h=0,lty="dashed",col="red")'	
	print >>RS, 'dev.off()'
if __name__ == '__main__':
	main()
