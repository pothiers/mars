#!/bin/bash -e
# PURPOSE: Update audit records for a batch of files (TADA like behavior).
#   Simulate attempt to ingest with Reject or Accept.
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
PROB=50 # 50% chance of (simulated) ingest Success

usage="USAGE: $cmd [options] file ...
OPTIONS:
  -d <day>::        YYYY-MM-DD of observation (default=$DAY)
  -i <instrument>:: Observing instrument (default=$INS)
  -t <telescope>::  Observing telescope (default=$TEL)
  -p <probality>::  Probability of (simulated) success [0..100] (default=$PROB)
  -u <uri>::        URI of web service (default=$URI)
  -v <verbosity>::  higher number for more output (default=$VERBOSE)
"

while getopts "hd:i:t:s:p:u:v:" opt; do
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
	p)
            PROB=$OPTARG # Probability of (simulated) success
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

##############################################################################

JSONFILE="/tmp/audit.$$.json"
extra="\"obsday\": \"$DAY\", \"telescope\": \"$TEL\", \"instrument\": \"$INS\""
echo '{ "observations": [' > $JSONFILE
oblist=""
for f; do
    md5=`md5sum $f | awk '{print $1}'`
    obj="\"md5sum\": \"$md5\", \"srcpath\": \"$f\"" 

    # Random success/fail
    x=`shuf -i 1-100 -n 1`
    NOW=`date '+%Y-%m-%d %H:%M:%S'`
    if [ $x -le $PROB ]; then
	SUCCESS="true"
	obj="$obj ,\"archfile\": \"kww_141220_130138_ori_TADASMOKE.fits.fz\""
    else
	SUCCESS="false"
	obj="$obj ,\"archerr\": \"Fake error from $0\""
    fi
    obj="$obj ,\"success\": $SUCCESS"
    obj="$obj ,\"submitted\": \"$NOW\""
    oblist="$oblist { $obj,  $extra},"
    


done
echo $oblist | sed "s/,$//" >> $JSONFILE
echo '] }' >> $JSONFILE

echo "Wrote: $JSONFILE"


curl -H "Content-Type: application/json" -d @$JSONFILE $URI
#rm $JSONFILE
