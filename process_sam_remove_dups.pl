use warnings;
use strict;

my $dup_count = 0;
my $curr_chr_read1;
my $curr_start_read1;
my $curr_chr_read2;
my $curr_start_read2;
#Data needs to be ordered by position...
open(FILE,$ARGV[0]);
while(<FILE>){
	chomp;
	#sys.stdout.write(read1.qname+"\t"+f1.getrname(read1.tid)+"\t"+str(read1_start)+"\t"+str(read1_end)+"\t"+str(read1.is_reverse)+"\t"+str(read1_unique))
	#sys.stdout.write("\t"+read2.qname+"\t"+f1.getrname(read2.tid)+"\t"+str(read2_start)+"\t"+str(read2_end)+"\t"+str(read2.is_reverse)+"\t"+str(read2_unique))
	my @data  = split(/\t/);
	my $read1_chr = $data[1];
	my $read1_start = $data[2];
	my $read2_chr = $data[7];
	my $read2_start = $data[8];
	#print $read1_chr."\t".$read1_start."\t".$read2_chr."\t".$read2_start."\n";
	if($curr_chr_read1){
		if(($read1_chr eq $curr_chr_read1) && ($curr_start_read1 == $read1_start) && 
		   ($read2_chr eq $curr_chr_read2) && ($curr_start_read2 == $read2_start)){
			$dup_count++;
		} else {
			print join("\t",@data)."\t".$dup_count."\n";
			$dup_count = 0;
		}
	}
	$curr_chr_read1 = $read1_chr;
	$curr_start_read1 = $read1_start;
	$curr_chr_read2 = $read2_chr;
	$curr_start_read2 = $read2_start;

}
close(FILE);
