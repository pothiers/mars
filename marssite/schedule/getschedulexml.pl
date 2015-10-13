#!/usr/bin/perl -w

# Core taken from GETSCHEDULE  by S.Pothier
#
# usage: getschedulexml -tel=<telname> -date=<yyyy-mm-dd>
# EXAMPLE:
#   ./getschedulexml.pl -tel=wiyn -date=2015-09-01 > wiyn.2015-09-01.schedule.xml
#


use strict ;

use Getopt::Long;
use SOAP::Lite;
#use XML::XPath;
#use XML::XPath::XMLParser;

use LWP::Protocol::http; # to suppress the warning "possible typo" in the next statement
push(@LWP::Protocol::http::EXTRA_SOCK_OPTS, MaxLineLength => 0); # to remove the limit


my ($tel, $date);

GetOptions ('tel=s' => \$tel, 'date=s' => \$date);


# defaults for testing
$tel ||= 'kp4m';
$date ||= '2014-08-27'; # yyyy-mm-dd
my $response = SOAP::Lite
    -> uri ('http://www.noao.edu/Andes/ScheduleSearch')
    -> proxy ('http://www.noao.edu/cgi-bin/webservices/andes/dispatch.pl');

my $propXml;
my $result = $response->getProposalsScheduledOn ($tel, $date);
unless ($result->fault) {
    $propXml = $result->result ();
} else {
    print join ', ', $result->faultcode, $result->faultstring;
}
print $propXml
