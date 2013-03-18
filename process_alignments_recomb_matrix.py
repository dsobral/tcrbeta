import pysam
import sys

#Bam file with alignments
align_file = sys.argv[1]
#Bed file with tcr loci e.g. data/genome/ensembl_e68_tcrb_locus_features_NCBIM37.refseq.bed
tcrbeta_loci_file = sys.argv[2]
consider_read = sys.argv[3]

handle = open(tcrbeta_loci_file,"r")

## data
loci_list = []
loci_pos = {}
for line in handle:
	line = line.strip()
	array = line.split("\t")
	#loci
	loci_name = array[3]
	loci_start = array[1]
	loci_end = array[2]
	loci_list.append(loci_name)
	loci_pos[loci_name] = [loci_start, loci_end]
	#print array[3]+":"+array[1]+"-"+array[2]

handle.close()

##Test to see if all is well
#for loci in loci_list:
#	print loci+"\t"+loci_pos[loci][0]+"\t"+loci_pos[loci][1]
#sys.exit()
#OK

samfile = pysam.Samfile(align_file, "rb" )

loci_recomb_reads = {}
loci_recomb_reads_loci = {}
loci_transloc_reads = {}
loci_total_reads = {}
loci_unique_reads = {}
for loci in loci_list:
	#initialize
	loci_recomb_reads[loci] = 0
	loci_recomb_reads_loci[loci] = {}
	for loci2 in loci_list:
		loci_recomb_reads_loci[loci][loci2] = 0
	loci_transloc_reads[loci] = 0
	total_reads = 0
	unique_reads = 0
        for read in samfile.fetch('6',int(loci_pos[loci][0]),int(loci_pos[loci][1])):		
		if((int(consider_read) == 2) and read.is_read1): continue
		if((int(consider_read) == 1) and read.is_read2): continue
		total_reads = total_reads + 1
                tags = {}
                for tag in read.tags:
                        tags[tag[0]] = tag[1]
		#Only include reads that are uniquely mapped
		if( ('NH' in tags) and (tags['NH']==1) and (read.mapq>2) and (not read.is_secondary)):
			unique_reads = unique_reads + 1
			#total_reads = total_reads + 1
			if( (not read.mate_is_unmapped) and (read.rnext == read.tid) and (abs(read.tlen)>1000) ):
				#in this case we want the specific reads
				loci_recomb_reads[loci] = loci_recomb_reads[loci] + 1		
				#check where is the mate hitting (give a few bp of tolerance)
				for loci2 in loci_list:
					if((read.pnext < int(loci_pos[loci2][1])+25) and (read.pnext>int(loci_pos[loci2][0])-25)):
						loci_recomb_reads_loci[loci][loci2] = loci_recomb_reads_loci[loci][loci2] + 1			
			if( (not read.mate_is_unmapped) and (read.rnext != read.tid) ):
				loci_transloc_reads[loci] = loci_transloc_reads[loci] + 1			

	loci_total_reads[loci] = total_reads	
	loci_unique_reads[loci] = unique_reads

samfile.close()

sys.stdout.write("Loci\tTotalReads\tUniqueReads\tTranslocEvents\tRecombEvents")
for loci in loci_list:
	sys.stdout.write("\tRecomb_"+loci)
sys.stdout.write("\n")
for loci in loci_list:
	sys.stdout.write(loci+"\t"+str(loci_total_reads[loci])+"\t"+str(loci_unique_reads[loci])+"\t"+str(loci_transloc_reads[loci])+"\t"+str(loci_recomb_reads[loci]))
	for loci2 in loci_list:
		sys.stdout.write("\t"+str(loci_recomb_reads_loci[loci][loci2]))
	sys.stdout.write("\n")
