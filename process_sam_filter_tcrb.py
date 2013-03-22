import pysam
import sys

f1 = pysam.Samfile(sys.argv[1],'r')
f2 = pysam.Samfile(sys.argv[2],'r')

read1_chr6id = f1.gettid('6')
read2_chr6id = f2.gettid('6')

TCRB_CHR = '6'
TCRB_START = 40831296
TCRB_END = 41518371

#TCR_Loci
#data/genome/ensembl_e68_tcrb_locus_features_NCBIM37.refseq.bed
tcr_loci = {}
#read the loci
file = open(sys.argv[3],"r")
for line in file:
	line = line.strip()
	fields = line.split("\t")	
	#create a dictionary with each entry
	tcr_loci[fields[3]] = { 'start':int(fields[1]), 'end':int(fields[2]) }		


while True:
	try:
		read1 = f1.next()
		read2 = f2.next()

		read1_start = read1.pos
		read1_end = read1.pos + read1.rlen

		read2_start = read2.pos
		read2_end = read2.pos + read2.rlen

		#only care about things when both mates are mapped
		if(read1.is_unmapped or read2.is_unmapped):
			continue

		#Ignore if none of the reads is in chromosome 6
		if((read1.tid!=read1_chr6id) and (read2.tid!=read2_chr6id)):
			continue

		#setup tags in a more convenient way for random access
		tags1 = {} 
		for tag in read1.tags:
			tags1[tag[0]] = tag[1]
		tags2 = {}
		for tag in read2.tags:
			tags2[tag[0]] = tag[1]

		read1_unique = True
		if(('XM' in tags1) and (tags1['XM']>1)):
			read1_unique = False

		read2_unique = True
		if(('XM' in tags2) and (tags2['XM']>1)):
			read2_unique = False
		
		#read1.is_reverse 
		#read2.is_reverse
		
		#print pair if they fall in any of the tcrb loci
		is_locus = False
		for loci in tcr_loci:
			if((read1.tid==read1_chr6id) and (read1_start < tcr_loci[loci]['end']) and (read1_end > tcr_loci[loci]['start'])):
				is_locus=True
				break
			if((read2.tid==read2_chr6id) and (read2_start < tcr_loci[loci]['end']) and (read2_end > tcr_loci[loci]['start'])):
				is_locus=True
				break
		if(is_locus):
			sys.stdout.write(read1.qname+"\t"+f1.getrname(read1.tid)+"\t"+str(read1_start)+"\t"+str(read1_end)+"\t"+str(read1.is_reverse)+"\t"+str(read1_unique))
			sys.stdout.write("\t"+read2.qname+"\t"+f1.getrname(read2.tid)+"\t"+str(read2_start)+"\t"+str(read2_end)+"\t"+str(read2.is_reverse)+"\t"+str(read2_unique))
			sys.stdout.write("\n")			
		
	#StopIteration is launched when no more reads are in the file
	except StopIteration:
		break

f1.close()
f2.close()
