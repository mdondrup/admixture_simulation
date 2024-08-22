#!/usr/bin/env perl
use strict;
use warnings;
use Getopt::Std;

our ($opt_p); # default percentile

getopts('p:');

$opt_p ||= 99;

sub percentile {
    my ($p,$aref) = @_;
    my $percentile = int($p * $#{$aref}/100);
    return (sort {$a->[4] <=> $b->[4]} @$aref)[$percentile][4];

}



my @data = ();

my $chr = undef;

while (<>) {
    chomp;
    next if /^\s*$/; # skip blank lines
    next if /^Position/; # A header encountered
    #print $_,"\n";
    if (/\/\//) { 
	($chr) = /^\/\/(\d+)/;
	next;
    }
    die "Invalid format, undefined chromosome $_" unless defined $chr;
    my @l = split /\t/, $_;
    die "error, expected 5 columns, got ". (scalar @l) unless (scalar @l) == 5;
    push @data, ["chr$chr", int($l[3])-1, int($l[4]), '.', $l[1]]; 
}

my $perc = percentile($opt_p, \@data);


map {print join ("\t", @$_),"\n" if ($_->[4] > $perc )  } @data;


print STDERR "$opt_p -percentile: $perc \n";

#map {print join ("\t", @$_),"\n"} @data;
