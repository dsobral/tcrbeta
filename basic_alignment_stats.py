import pysam
import sys

#TCRb NCBIM37
TCRB_CHR = '6'       
TCRB_START = 40831296
TCRB_END = 41518371
#CAREFULL COORDINATES NCBIM38 are 50KB more

#file with alignments as first parameter
align_file = sys.argv[1]

samfile = pysam.Samfile(align_file, "rb" )

#print "File: "+align_file
unmapped = samfile.unmapped
#print "Unmapped reads: "+str(unmapped)
mappings = samfile.mapped
#print "Alignments: "+str(mappings)


#Table1 TCRb
#read1_totals = 0
#read1_mate_mapped = 0
#read2_totals = 0
#read2_mate_mapped = 0
#reads = samfile.fetch(TCRB_CHR,TCRB_START,TCRB_END)
#for read in reads:
#	#if(read.is_secondary): continue
#	#Make read1 and read2 counts independently...
#	if(read.is_read1):
#		read1_totals = read1_totals + 1
#		if(not read.mate_is_unmapped):
#			read1_mate_mapped = read1_mate_mapped + 1			
#	if(read.is_read2):
#		read2_totals = read2_totals + 1
#		if(not read.mate_is_unmapped):
#			read2_mate_mapped = read2_mate_mapped + 1			
#
#print str(read1_totals)+"\t"+str(read1_mate_mapped)+"\t"+str(read2_totals)+"\t"+str(read2_mate_mapped)



#Table2 Tcrb
#How long the insert length must be to be considered an "event"
#Quite arbitrary... distribution would suggest >200-300 might already be enough...
REC_THRESH=1000

read_correct_correct = 0
read_correct_reversed = 0
read_recomb_correct = 0
read_recomb_reversed = 0
read_trans = 0
reads = samfile.fetch(TCRB_CHR,TCRB_START,TCRB_END)
for read in reads:
	if(read.is_read1 and (not read.is_secondary) and (not read.mate_is_unmapped)):

#		multiple = False		
#		for tag in read.tags:
#			if((tag[0] == 'NH') and (tag[1]>1)):				
#				multiple = True				
#		if(multiple): continue
	
		reverse = False
		if( (not read.is_reverse) and (not read.mate_is_reverse)):
			reverse = True
		if(read.is_reverse and read.mate_is_reverse):
			reverse = True
		if(read.tid != read.rnext):
			read_trans = read_trans + 1
		else:
			if(abs(read.tlen)>1000):
				if(reverse):
					read_recomb_reversed = read_recomb_reversed + 1
				else:
					read_recomb_correct = read_recomb_correct + 1	
			else:
				if(reverse):
					read_correct_reversed = read_correct_reversed + 1
				else:
					read_correct_correct = read_correct_correct + 1

print "\tUnmapped\tAlignments\tPair_Correct\tPair_Reverse\tRecombine_Correct\tRecombine_Reverse\tTranslocations"

#print "TCRB(unique):\t"+str(read_correct_correct)+"\t"+str(read_correct_reversed)+"\t"+str(read_recomb_correct)+"\t"+str(read_recomb_reversed)+"\t"+str(read_trans)		
print "TCRB\t"+str(unmapped)+"\t"+str(mappings)+"\t"+str(read_correct_correct)+"\t"+str(read_correct_reversed)+"\t"+str(read_recomb_correct)+"\t"+str(read_recomb_reversed)+"\t"+str(read_trans)

unmapped mappings


read_correct_correct = 0
read_correct_reversed = 0
read_recomb_correct = 0
read_recomb_reversed = 0
read_trans = 0
read_trans_chr6 = 0

for ref in (samfile.references):

	#Ignore chromosome 6 (could only ignore Tcrbeta alternatively)
	if(ref == '6'): continue	

	reads = samfile.fetch(ref)
	for read in reads:

	       if(read.is_read1 and (not read.is_secondary) and (not read.mate_is_unmapped)):
	               reverse = False

	               #Remove Tag afterwards
#        	       multiple = False                
#	               for tag in read.tags:
#        	               if((tag[0] == 'NH') and (tag[1]>1)):                            
#                	               multiple = True
#	               if(multiple): continue

	               if( (not read.is_reverse) and (not read.mate_is_reverse)):
	                       reverse = True
	               if(read.is_reverse and read.mate_is_reverse):
	                       reverse = True

	               if(read.tid != read.rnext):
                               read_trans = read_trans + 1
                               if(samfile.getrname(read.rnext) == '6'):
                                       read_trans_chr6 = read_trans_chr6 + 1				
	               else:
	                       if(abs(read.tlen)>1000):
	                               if(reverse):
	                                       read_recomb_reversed = read_recomb_reversed + 1
	                               else:
	                                       read_recomb_correct = read_recomb_correct + 1   
	                       else:
	                               if(reverse):
	                                       read_correct_reversed = read_correct_reversed + 1
	                               else:
	                                       read_correct_correct = read_correct_correct + 1
	
#print "All(except chr6; unique):\t"+str(read_correct_correct)+"\t"+str(read_correct_reversed)+"\t"+str(read_recomb_correct)+"\t"+str(read_recomb_reversed)+"\t"+str(read_trans)+"\t"+str(read_trans_chr6)
print "All\t"+str(unmapped)+"\t"+str(mappings)+"\t"+str(read_correct_correct)+"\t"+str(read_correct_reversed)+"\t"+str(read_recomb_correct)+"\t"+str(read_recomb_reversed)+"\t"+str(read_trans)
