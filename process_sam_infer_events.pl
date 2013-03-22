use warnings;
use strict;

#e.g. data/genome/ensembl_e68_tcrb_locus_features_NCBIM37.refseq.bed
my %tcr_loci;
open(FILE,$ARGV[1]);
while(<FILE>){
	chomp;
	my ($chr,$start,$end,$name) = split(/\t/);
	#print $name."\t".$chr."\t".$start."\t".$end."\n";
	$tcr_loci{$name}{'start'} = $start;
	$tcr_loci{$name}{'end'} = $end;
}
close FILE;

open(FILE,$ARGV[0]);
while(<FILE>){
	chomp;
	my (undef,$chr1,$start1,$end1,$is_reverse1,$is_unique1,undef,$chr2,$start2,$end2,$is_reverse2,$is_unique2) = split(/\t/);	
	#print $chr1."\t".$start1."\t".$end1."\t".$is_reverse1."\t".$is_unique1."\t".$chr2."\t".$start2."\t".$end2."\t".$is_reverse2."\t".$is_unique2."\n";
	if(($is_unique1 eq 'False') || ($is_unique2 eq 'False')){
		print "NON_UNIQUE_MAPPING\n";
	} else {
		my $order = "OK";
		if($is_reverse1 eq $is_reverse2) { $order = "NOK"; }

		my $type1 = type($chr1,$start1,$end1);
		my $type2 = type($chr2,$start2,$end2);
		
		if($type1 eq $type2){
			print $type1."\tOK\t".$type2."\t".$order."\n";
		} else {
			if($type1 eq "NON_CHR6"){
				print $type2."\t"."TRANS\tNA\tNA\n";
			} else {
				if($type2 eq "NON_CHR6"){
					print $type1."\tTRANS\tNA\tNA\n";
				} else {
					print $type1."\tRECOMB\t".$type2."\t".$order."\n";
				}
			}
		}
		
	}
}
close FILE;

sub type {
	my ($chr, $start, $end) = (shift, shift, shift);
	if($chr ne '6'){ 
		return "NON_CHR6";
	} else {
		my $tcr = "CHR6_NOTCR";
		foreach my $loci (keys %tcr_loci){	
			if(($start<$tcr_loci{$loci}{'end'}) && ($end>$tcr_loci{$loci}{'start'})){
				$tcr = $loci;
				last;	
			}
		}
		return $tcr;
	}		
}
