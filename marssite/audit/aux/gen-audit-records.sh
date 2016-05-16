#!/bin/bash -e
# PURPOSE: Add initial audit records for a batch of files
#
# EXAMPLE:
#
# AUTHORS: S.Pothier

SCRIPT=$(readlink -f $0)        # Absolute path to this script
SCRIPTPATH=$(dirname $SCRIPT)   # Absolute path this script is in

VERBOSE=0
URI="http://localhost:8000/audit/source/"
DAY=`date '+%Y-%m-%d'`
INS="unknown"
TEL="unknown"

usage="USAGE: $cmd [options] file ...
OPTIONS:
  -d <day>::        YYYY-MM-DD of observation (default=$DAY)
  -i <instrument>:: Observing instrument (default=$INS)
  -t <telescope>::  Observing telescope (default=$TEL)
  -u <uri>::        URI of web service (default=$URI)
  -v <verbosity>::  higher number for more output (default=$VERBOSE)
"

while getopts "hd:i:t:s:v:" opt; do
    #! echo "opt=<$opt>"
    case $opt in
	h)
            echo "$usage"
            exit 1
            ;;
        v)
            VERBOSE=$OPTARG
            ;;
        d)
            DAY=$OPTARG # Day observed
            ;;
        i)
            INS=$OPTARG # Instrument
            ;;
        t)
            TEL=$OPTARG # Telescope
            ;;
        u)
            URI=$OPTARG # URI for web service
            ;;
        \?)
            echo "Invalid option: -$OPTARG" >&2
            exit 1
            ;;
        :)
            echo "Option -$OPTARG requires an argument." >&2
            exit 1
            ;;
    esac
done
#echo "OPTIND=$OPTIND"
for (( x=1; x<$OPTIND; x++ )); do shift; done

RAC=1 # Required Argument Count
if [ $# -lt $RAC ]; then
    echo "Not enough non-option arguments. Expect at least $RAC."
    echo >&2 "$usage"
    exit 2
fi


#! echo "PROGRESS=$PROGRESS"
#! echo "VERBOSE=$VERBOSE"
#! echo "Remaining arguments:"
#! for arg do echo '--> '"\`$arg'" ; done
##############################################################################



#curl -H "Content-Type: application/json" -d '{ "observations": [ { "md5sum": "c89350d2f507a883bc6a3e9a6f418a13", "obsday": "2016-05-12", "telescope": "kp09m", "instrument": "whirc", "srcpath": "/data/20165012/foo3.fits" } ] }' http://localhost:8000/audit/source/

#json='{ "observations": [ { "md5sum": "c89350d2f507a883bc6a3e9a6f418a13", "obsday": "2016-05-12", "telescope": "kp09m", "instrument": "whirc", "srcpath": "/data/20165012/foo3.fits" } ] }'


JSONFILE="/tmp/audit.$$.json"
extra="\"obsday\": \"$DAY\", \"telescope\": \"$TEL\", \"instrument\": \"$INS\""
echo '{ "observations": [' > $JSONFILE
oblist=""
for f; do
    md5=`md5sum $f | awk '{print $1}'`
    oblist="$oblist { \"md5sum\": \"$md5\", \"srcpath\": \"$f\", $extra }," 
done
echo $oblist | sed "s/,$//" >> $JSONFILE
echo '] }' >> $JSONFILE

#echo "Wrote: $JSONFILE"

curl -H "Content-Type: application/json" -d @$JSONFILE $URI
rm $JSONFILE
