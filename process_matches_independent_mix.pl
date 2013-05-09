use warnings;
use strict;

#TRBV1   8       84      FREDDYKRUEGER_0073:3:59:3100:4239#0     25      -       76M
#print $ARGV[0]."\n";
#print $ARGV[1]."\n";

my %read_pairs;
open(FILE,$ARGV[0]);
while(<FILE>){
	chomp;
	my ($feat_name, $start, $end, $read_name, undef, $strand) = split(/\t/);
	$read_pairs{$read_name}{1}{'feat_name'} = uc($feat_name);
	$read_pairs{$read_name}{1}{'strand'} = $strand;
	$read_pairs{$read_name}{1}{'start'} = $start;
	$read_pairs{$read_name}{1}{'end'} = $end;
}	
close FILE;

open(FILE,$ARGV[1]);
while(<FILE>){
	chomp;
	my ($feat_name, $start, $end, $read_name, undef, $strand) = split(/\t/);
	$read_pairs{$read_name}{2}{'feat_name'} = uc($feat_name);
	$read_pairs{$read_name}{2}{'strand'} = $strand;
	$read_pairs{$read_name}{2}{'start'} = $start;
	$read_pairs{$read_name}{2}{'end'} = $end;
}	
close FILE;


my @recomb_pairs;
foreach my $read (keys %read_pairs){
	if(defined($read_pairs{$read}{1}) && defined($read_pairs{$read}{2})){
		if( ( ($read_pairs{$read}{1}{'feat_name'} =~ /TRBV/) && ($read_pairs{$read}{2}{'feat_name'} =~ /TRBJ/) ) ||
 	 	    ( ($read_pairs{$read}{2}{'feat_name'} =~ /TRBV/) && ($read_pairs{$read}{1}{'feat_name'} =~ /TRBJ/ ) ) 		
		# This situation only happens for TRBV12.2 and TRBV13.2 
		#if( ( ($read_pairs{$read}{1}{'feat_name'} =~ /TRBV/) && ($read_pairs{$read}{2}{'feat_name'} =~ /TRBV/) ) && 
		#	( ($read_pairs{$read}{1}{'feat_name'} ne  $read_pairs{$read}{2}{'feat_name'}) )
		  ) {

			push(@recomb_pairs, $read); 
			#print $read;
			#print "\t".$read_pairs{$read}{1}{'feat_name'}."\t".$read_pairs{$read}{1}{'start'}."\t".$read_pairs{$read}{1}{'end'}."\t".$read_pairs{$read}{1}{'strand'};
			#print "\t".$read_pairs{$read}{2}{'feat_name'}."\t".$read_pairs{$read}{2}{'start'}."\t".$read_pairs{$read}{2}{'end'}."\t".$read_pairs{$read}{2}{'strand'};
			#print "\n";
		}
	}
}


#now remove duplicates (just keep a single copy of each)
my @non_dup;
foreach my $read (@recomb_pairs){
	my $dup = 0;
	foreach my $current (@non_dup){
		#use only start
		my $st1 =  $read_pairs{$read}{1}{'start'};
		my $end1 = $read_pairs{$read}{2}{'start'};
		my $st2 = $read_pairs{$current}{1}{'start'};
		my $end2 = $read_pairs{$current}{2}{'start'};
		if(($st1 == $st2) && ($end1 == $end2)){
			$dup = 1;
			last;
		}
	}
	if(!$dup){
		push(@non_dup, $read);
	}
}

#finally print non_duplicate entries;
foreach my $read (@non_dup){
	#print $read;
	#if($read_pairs{$read}{1}{'feat_name'} =~ /TRBV/){
	#        print "\t".$read_pairs{$read}{1}{'feat_name'}."\t".$read_pairs{$read}{1}{'start'}."\t".$read_pairs{$read}{1}{'end'}."\t".$read_pairs{$read}{1}{'strand'};
	#        print "\t".$read_pairs{$read}{2}{'feat_name'}."\t".$read_pairs{$read}{2}{'start'}."\t".$read_pairs{$read}{2}{'end'}."\t".$read_pairs{$read}{2}{'strand'};
	#        print "\n"; 
	#} else {
	#when TRBV is in 1, it's probably reverse transcripts... found ~4 cases, 2 for TRBV13.2 and 2 for TRBV4
	if($read_pairs{$read}{2}{'feat_name'} =~ /TRBV/){
		print $read;
	        print "\t".$read_pairs{$read}{2}{'feat_name'}."\t".$read_pairs{$read}{2}{'start'}."\t".$read_pairs{$read}{2}{'end'}."\t".$read_pairs{$read}{2}{'strand'};
	        print "\t".$read_pairs{$read}{1}{'feat_name'}."\t".$read_pairs{$read}{1}{'start'}."\t".$read_pairs{$read}{1}{'end'}."\t".$read_pairs{$read}{1}{'strand'};
	        print "\n"; 
	}
}
