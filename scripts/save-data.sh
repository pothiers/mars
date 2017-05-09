#!/bin/bash -e
# PURPOSE: Save DB data from MARS apps
#
# EXAMPLE:
#   source ../venv/bin/activate
#   ./save-data.sh
#
# AUTHORS: S.Pothier

cmd=`basename $0`
dir=`dirname $0`

SCRIPT=$(readlink -f $0)      #Absolute path to this script
SCRIPTPATH=$(dirname $SCRIPT) #Absolute path this script is in
MARSROOT=$(dirname $SCRIPTPATH)

usage="USAGE: $cmd [options] [reportFile]
OPTIONS:
  -p <progress>:: Number of progress updates per second (default=0)
  -v <verbosity>:: higher number for more output (default=0)

"

VERBOSE=0
PROGRESS=0
while getopts "hp:v:" opt; do
    echo "opt=<$opt>"
    case $opt in
	    h)
            echo "$usage"
            exit 1
            ;;
        v)
            VERBOSE=$OPTARG
            ;;
        p)
            PROGRESS=$OPTARG # how often to report progress
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


echo "PROGRESS=$PROGRESS"
echo "VERBOSE=$VERBOSE"
echo "Remaining arguments:"
for arg do echo '--> '"\`$arg'" ; done

report=${1:-$HOME/logs/foo.report}

apps="
audit
natica
provisional
schedule
tada
water
"
#!siap  # not managed, uses legacy "metadata" database

stamp=`date '+%Y.%m.%d_%H.%M'`
hash=`git rev-parse --verify HEAD`
dir=$HOME/data/mars/${hash}
mkdir -p ${dir} > /dev/null
date > $dir/STAMP.txt
echo $hash > $dir/HASH.txt # git snapshot

mir="sdmvm1.tuc.noao.edu:/repo/mirrors/mars-data"

#DJANGO_SETTINGS_MODULE=marssite.marssite.settings

##############################################################################

SITE=$MARSROOT/marssite
echo "SITE=$SITE"
pushd $SITE
for app in $apps
do
    outfile=$dir/${app}.yaml
    echo "Writing: $outfile"
    $SITE/manage.py dumpdata --format=yaml --indent=4 --output=$outfile $app
done

echo "Syncing $dir to $mir"
rsync -avz $dir $mir
