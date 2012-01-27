#!/usr/bin/env python
'''-------------------------------------------------------------------------------------------------
Check reads distribution over exon, intron, UTR, intergenic ... etc
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

#import third-party modules
from bx.bitset import *
from bx.bitset_builders import *
from bx.intervals import *
from bx.binned_array import BinnedArray
from bx_extras.fpconst import isNaN
from bx.bitset_utils import *


#import my own modules
from qcmodule import BED
from qcmodule import SAM


__author__ = "Liguo Wang"
__copyright__ = "Copyright 2010, Wei Li's Lab"
__credits__ = []
__license__ = "GPL"
__version__="1.0.5"
__maintainer__ = "Liguo Wang"
__email__ = "liguow@bcm.edu"
__status__ = "Development" #Prototype or Production

def base_read(lst,rang):
	base=0
	read=0
	for i in lst:
		base += i[2]-i[1]
		if i[0].upper() in rang:
			read += len(rang[i[0].upper()].find(i[1],i[2]))
	return (base,read)

def main():
	usage="%prog [options]" + '\n' + __doc__ + "\n"
	parser = OptionParser(usage,version="%prog " + __version__)
	parser.add_option("-i","--input-file",action="store",type="string",dest="input_file",help="Input file in SAM format. Use \"-\" represents standard input [required]")
	parser.add_option("-r","--refgene",action="store",type="string",dest="ref_gene_model",help="Reference gene model in bed format. [required]")
	(options,args)=parser.parse_args()
		
	if not (options.input_file and options.ref_gene_model):
		parser.print_help()
		sys.exit(0)
	if not os.path.exists(options.ref_gene_model):
		print >>sys.stderr, '\n\n' + options.ref_gene_model + " does NOT exists" + '\n'
		#parser.print_help()
		sys.exit(0)
	if os.path.exists(options.input_file):
		file_obj=open(options.input_file)
		pass
	elif options.input_file == '-':
		file_obj=sys.stdin
		pass
	else:
		print >>sys.stderr, '\n\n' + options.input_file + " does NOT exists" + '\n'
		#parser.print_help()
		sys.exit(0)		
	print >>sys.stderr, "processing " + options.ref_gene_model + ' ...',
	obj = BED.ParseBED(options.ref_gene_model)
	utr_3 = obj.getUTR(utr=3)
	utr_5 = obj.getUTR(utr=5)
	cds_exon = obj.getCDSExon()
	intron = obj.getIntron()
	
	intron = BED.unionBed3(intron)
	cds_exon=BED.unionBed3(cds_exon)
	utr_5 = BED.unionBed3(utr_5)
	utr_3 = BED.unionBed3(utr_3)
	
	utr_5 = BED.subtractBed3(utr_5,cds_exon)
	utr_3 = BED.subtractBed3(utr_3,cds_exon)
	intron = BED.subtractBed3(intron,cds_exon)
	intron = BED.subtractBed3(intron,utr_5)
	intron = BED.subtractBed3(intron,utr_3)
	
	intergenic_up_1kb = obj.getIntergenic(direction="up",size=1000)
	intergenic_down_1kb = obj.getIntergenic(direction="down",size=1000)
	intergenic_up_5kb = obj.getIntergenic(direction="up",size=5000)
	intergenic_down_5kb = obj.getIntergenic(direction="down",size=5000)	
	intergenic_up_10kb = obj.getIntergenic(direction="up",size=10000)
	intergenic_down_10kb = obj.getIntergenic(direction="down",size=10000)
	
	#merge integenic region
	intergenic_up_1kb=BED.unionBed3(intergenic_up_1kb)
	intergenic_up_5kb=BED.unionBed3(intergenic_up_5kb)
	intergenic_up_10kb=BED.unionBed3(intergenic_up_10kb)
	intergenic_down_1kb=BED.unionBed3(intergenic_down_1kb)
	intergenic_down_5kb=BED.unionBed3(intergenic_down_5kb)
	intergenic_down_10kb=BED.unionBed3(intergenic_down_10kb)	
	
	#purify intergenic region
	intergenic_up_1kb=BED.subtractBed3(intergenic_up_1kb,cds_exon)
	intergenic_up_1kb=BED.subtractBed3(intergenic_up_1kb,utr_5)
	intergenic_up_1kb=BED.subtractBed3(intergenic_up_1kb,utr_3)
	intergenic_up_1kb=BED.subtractBed3(intergenic_up_1kb,intron)
	intergenic_down_1kb=BED.subtractBed3(intergenic_down_1kb,cds_exon)
	intergenic_down_1kb=BED.subtractBed3(intergenic_down_1kb,utr_5)
	intergenic_down_1kb=BED.subtractBed3(intergenic_down_1kb,utr_3)
	intergenic_down_1kb=BED.subtractBed3(intergenic_down_1kb,intron)	

	#purify intergenic region
	intergenic_up_5kb=BED.subtractBed3(intergenic_up_5kb,cds_exon)
	intergenic_up_5kb=BED.subtractBed3(intergenic_up_5kb,utr_5)
	intergenic_up_5kb=BED.subtractBed3(intergenic_up_5kb,utr_3)
	intergenic_up_5kb=BED.subtractBed3(intergenic_up_5kb,intron)
	intergenic_down_5kb=BED.subtractBed3(intergenic_down_5kb,cds_exon)
	intergenic_down_5kb=BED.subtractBed3(intergenic_down_5kb,utr_5)
	intergenic_down_5kb=BED.subtractBed3(intergenic_down_5kb,utr_3)
	intergenic_down_5kb=BED.subtractBed3(intergenic_down_5kb,intron)	
	
	#purify intergenic region
	intergenic_up_10kb=BED.subtractBed3(intergenic_up_10kb,cds_exon)
	intergenic_up_10kb=BED.subtractBed3(intergenic_up_10kb,utr_5)
	intergenic_up_10kb=BED.subtractBed3(intergenic_up_10kb,utr_3)
	intergenic_up_10kb=BED.subtractBed3(intergenic_up_10kb,intron)
	intergenic_down_10kb=BED.subtractBed3(intergenic_down_10kb,cds_exon)
	intergenic_down_10kb=BED.subtractBed3(intergenic_down_10kb,utr_5)
	intergenic_down_10kb=BED.subtractBed3(intergenic_down_10kb,utr_3)
	intergenic_down_10kb=BED.subtractBed3(intergenic_down_10kb,intron)	
	
	print >>sys.stderr, "Done"
	
	ranges={}
	totalReads=0
	spliceReads=0
	cUR=0
	multiMapReads=0
	
	print >>sys.stderr, "reading SAM file",
	for line in file_obj:
		if line.startswith("@"):continue
		fields=line.rstrip('\n ').split()
		flagCode=string.atoi(fields[1])
		if (flagCode & 0x0004) != 0: continue		#skip unmap reads
		totalReads +=1
		if not SAM.ParseSAM._uniqueHit_pat.search(line):		#skip multiple mapped reads
			multiMapReads +=1
			continue

		chrom = fields[2].upper()
		chromStart = string.atoi(fields[3])-1
		comb=[int(i) for i in SAM.ParseSAM._splicedHit_pat.findall(fields[5])]	#"9M4721N63M3157N8M" return ['9', '4721', '63', '3157', '8']
		cUR += (len(comb) +1)/2
		if(len(comb)>1):
			spliceReads += 1
		blockStart=[]
		blockSize=[]
			
		for i in range(0,len(comb),2):
			blockStart.append(chromStart + sum(comb[:i]) )
				
		for i in range(0,len(comb),2):
			blockSize.append(comb[i])
			
		for st,size in zip(blockStart,blockSize):
			mid = int(st) + (size/2)
			if chrom not in ranges:
				ranges[chrom] = Intersecter()
			else:
				ranges[chrom].add_interval( Interval( mid, mid ) )
	print >>sys.stderr, "Done"
	print >>sys.stderr, "Total Reads: " + str(totalReads)
	print >>sys.stderr, "Multiple Hits: " + str(multiMapReads)
	print >>sys.stderr, "Unique Hits: " + str(totalReads-multiMapReads)
	print >>sys.stderr, "Spliced Hits: " + str(spliceReads)
	print >>sys.stderr, "Total fragments: " + str(cUR)
	
	
	
	print >>sys.stderr, "\nAssignning reads ...",
	intron_read=0
	intron_base=0
	cds_exon_read=0
	cds_exon_base=0
	utr_5_read=0
	utr_5_base=0
	utr_3_read=0
	utr_3_base=0
	
	intergenic_up1kb_base=0
	intergenic_up1kb_read=0
	intergenic_down1kb_base=0
	intergenic_down1kb_read=0
	intergenic_up5kb_base=0
	intergenic_up5kb_read=0
	intergenic_down5kb_base=0
	intergenic_down5kb_read=0
	intergenic_up10kb_base=0
	intergenic_up10kb_read=0
	intergenic_down10kb_base=0
	intergenic_down10kb_read=0	
	
	(intron_base,intron_read) = base_read(intron,ranges)
	(cds_exon_base,cds_exon_read) = base_read(cds_exon,ranges)
	(utr_5_base,utr_5_read) = base_read(utr_5,ranges)
	(utr_3_base,utr_3_read) = base_read(utr_3,ranges)
	(intergenic_up1kb_base, intergenic_up1kb_read) = base_read(intergenic_up_1kb,ranges)
	(intergenic_up5kb_base, intergenic_up5kb_read) = base_read(intergenic_up_5kb,ranges)
	(intergenic_up10kb_base, intergenic_up10kb_read) = base_read(intergenic_up_10kb,ranges)
	(intergenic_down1kb_base, intergenic_down1kb_read) = base_read(intergenic_down_1kb,ranges)
	(intergenic_down5kb_base, intergenic_down5kb_read) = base_read(intergenic_down_5kb,ranges)
	(intergenic_down10kb_base, intergenic_down10kb_read) = base_read(intergenic_down_10kb,ranges)
	
	print >>sys.stderr, "Done"
	
	print >>sys.stderr, "========================================================="
	print >>sys.stderr, "Group\tTotal_bases\tReads_count\tReads/Kb"
	print >>sys.stderr, "CDS Exons:\t%d\t%d\t%5.2f" % (cds_exon_base,cds_exon_read,cds_exon_read*1000.0/cds_exon_base)
	print >>sys.stderr, "5'UTR Exons:\t%d\t%d\t%5.2f" % (utr_5_base,utr_5_read, utr_5_read*1000.0/utr_5_base)
	print >>sys.stderr, "3'UTR Exons:\t%d\t%d\t%5.2f" % (utr_3_base,utr_3_read, utr_3_read*1000.0/utr_3_base)
	print >>sys.stderr, "Intronic region:\t%d\t%d\t%5.2f" % (intron_base,intron_read,intron_read*1000.0/intron_base)
	
	print >>sys.stderr, "TSS up 1kb:\t%d\t%d\t%5.2f" % (intergenic_up1kb_base, intergenic_up1kb_read, intergenic_up1kb_read*1000.0/intergenic_up1kb_base)
	print >>sys.stderr, "TSS up 5kb:\t%d\t%d\t%5.2f" % (intergenic_up5kb_base, intergenic_up5kb_read, intergenic_up5kb_read*1000.0/intergenic_up5kb_base)
	print >>sys.stderr, "TSS up 10kb:\t%d\t%d\t%5.2f" % (intergenic_up10kb_base, intergenic_up10kb_read, intergenic_up10kb_read*1000.0/intergenic_up10kb_base)
	print >>sys.stderr, "TES down 1kb:\t%d\t%d\t%5.2f" % (intergenic_down1kb_base, intergenic_down1kb_read, intergenic_down1kb_read*1000.0/intergenic_down1kb_base)
	print >>sys.stderr, "TES down 5kb:\t%d\t%d\t%5.2f" % (intergenic_down5kb_base, intergenic_down5kb_read, intergenic_down5kb_read*1000.0/intergenic_down5kb_base)	
	print >>sys.stderr, "TES down 10kb:\t%d\t%d\t%5.2f" % (intergenic_down10kb_base, intergenic_down10kb_read, intergenic_down10kb_read*1000.0/intergenic_down10kb_base)
	print >>sys.stderr, "========================================================="
if __name__ == '__main__':
	main()
