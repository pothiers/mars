#!/bin/bash -e
# PURPOSE: Load previously saved DB data into MARS apps
# EXAMPLE:
#   ./load-data.sh
#

cmd=`basename $0`
dir=`dirname $0`

SCRIPT=$(readlink -f $0)      #Absolute path to this script
SCRIPTPATH=$(dirname $SCRIPT) #Absolute path this script is in
MARSROOT=$(dirname $SCRIPTPATH)

VERBOSE=0
datadir=$HOME/Download/marsdata
mirrdir="sdmvm1.tuc.noao.edu:/repo/mirrors/mars-data"

usage="USAGE: $cmd [options] 
OPTIONS:
  -d <datadir>:: Directory containing DB content as YAML files. [dflt: $datadir]
  -v <verbosity>:: higher number for more output (default=0)

"

while getopts "hd:v:" opt; do
    case $opt in
	    h)
            echo "$usage"
            exit 1
            ;;
        d)
            datadir=$OPTARG
            ;;
        v)
            VERBOSE=$OPTARG
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


RAC=0 # Required Argument Count
if [ $# -lt $RAC ]; then
    echo "Not enough non-option arguments. Expect at least $RAC."
    echo >&2 "$usage"
    exit 2
fi

apps="
audit
natica
provisional
schedule
tada
water
"
#!siap  # not managed, uses legacy "metadata" database

##############################################################################

SITE=$MARSROOT/marssite
#echo "SITE=$SITE"
pushd $SITE
source $MARSROOT/venv/bin/activate


#!stamp=`date '+%Y.%m.%d_%H.%M'`
#!hash=`git rev-parse --verify HEAD`
mkdir -p ${datadir} > /dev/null

echo "Syncing $mirrdir to $datadir"
rsync -avz $mirrdir/ $datadir/

newest=`ls -trd $datadir/*/ | tail -1`
hashdir=${newest%?}

STAMP=`cat $hashdir/STAMP.txt`
HASH=`cat $hashdir/HASH.txt`

echo
echo "Using data saved: $STAMP"
echo "Corresponding to git hash: $HASH"
echo "Storing data in: $hashdir"
echo

for app in $apps
do
    fixture=$hashdir/${app}.yaml
    echo "DRY-RUN from: $fixture" 
    #!echo "Loading from: $fixture" 
    #! $SITE/manage.py loaddata $fixture
done
