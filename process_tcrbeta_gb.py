import sys
from Bio import SeqIO

input_handle = open(sys.argv[1], "rU")
tcrbeta_record = SeqIO.parse(input_handle, "genbank").next()
for feature in tcrbeta_record.features:
	if( feature.type in ('C_region','D_segment','V_segment','J_segment')): 
		name = feature.qualifiers['standard_name'][0]		
		seq = ''
		if(len(feature.sub_features)>0):
			for subfeature in feature.sub_features:
				seq = seq + subfeature.extract(tcrbeta_record.seq)
		else:
			seq = feature.extract(tcrbeta_record.seq)
		print ">"+name+"\n"+seq
			
#	if my_snp in feature:
#		print feature.type, feature.qualifiers.get('db_xref')


#for record in SeqIO.parse(input_handle, "genbank") :
#    print record
#input_handle.close()

#print sys.argv[1]
#print sys.argv[2]
#count = SeqIO.convert(sys.argv[1], "genbank", sys.argv[2], "fasta")
#print "Converted %i records" % count
