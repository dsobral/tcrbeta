import pysam
import sys

align_file = sys.argv[1]
samfile = pysam.Samfile(align_file, "rb" )

#Draw an estimate from the region where we're supposed to be enriching
for read in samfile.fetch('6',40831296,41518371):
	#Only plot those mapping in the same chromosome...
	if((not read.is_unmapped) and (not read.mate_is_unmapped) and (read.tid == read.rnext)):
		if(read.is_read1):
			if(not read.is_reverse):
				if(read.mate_is_reverse):
					print abs(read.tlen)
			else:				
				if(not read.mate_is_reverse):
					print abs(read.tlen)

samfile.close()
