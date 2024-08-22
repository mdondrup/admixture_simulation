#!/usr/bin/env perl

use strict;
use warnings;
open ANNOT, $ARGV[0] || die "couldn't open annotation file $ARGV[0]: $!";
my %h = ();
my @samples = ();
while (<STDIN>) {
   push @samples, (split /\s/);
}
#print join "\n", @samples;
#exit 1;
while (my $ann = <ANNOT>) {
  chomp $ann;
  my @l = split /\t/, $ann;
  next unless $l[0];
  $h{$l[0]} = $l[5];
}

foreach my $sample (@samples) {

   if ($sample =~ /^sample/) {
      print $sample,"\t",$sample,"\tKveik\n";
      next; 
   }

   my ($id,$id2, @rest) = split /\./, $sample;
   if (! exists $h{$id} ) {
      warn "didn't find '$id', extending $id2";
      $id .= ".$id2";
   } 
   if (! exists $h{$id} ) {
      die "Group annotation not found for $sample : $id; need to remove it from the input";
      next;
   }

  $h{$id} =~ s/\s/_/g; 
   print $sample,"\t",$sample,"\t", $h{$id} ,"\n";
   
}
