#!/bin/bash -e
# PURPOSE: Save DB data from MARS apps
#
# EXAMPLE:
#   ./save-data.sh
#
# TODO:
#   add TAG.txt file indicating associaged git tag (if any) of commit

cmd=`basename $0`
dir=`dirname $0`

SCRIPT=$(readlink -f $0)      #Absolute path to this script
SCRIPTPATH=$(dirname $SCRIPT) #Absolute path this script is in
MARSROOT=$(dirname $SCRIPTPATH)

VERBOSE=0
stamp=`date '+%Y.%m.%d_%H.%M'`
hash=`git rev-parse --verify HEAD`
datadir="$HOME/data/mars/${hash}"
mirrdir="sdmvm1.tuc.noao.edu:/repo/mirrors/mars-data/${hash}"


usage="USAGE: $cmd [options]
OPTIONS:
  -d <datadir>:: Directory to store DB content as YAML files. [dflt: $datadir]
  -v <verbosity>:: higher number for more output (default=$VERBOSE)

"


while getopts "hd:v:" opt; do
    echo "opt=<$opt>"
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

mkdir -p ${datadir} > /dev/null
date > $datadir/STAMP.txt
echo $hash > $datadir/HASH.txt # git snapshot


#DJANGO_SETTINGS_MODULE=marssite.marssite.settings

##############################################################################

SITE=$MARSROOT/marssite
echo "SITE=$SITE"
pushd $SITE

source $MARSROOT/venv/bin/activate

echo "Saving data as of: $STAMP"
echo "Corresponding to git hash: $HASH"
for app in $apps
do
    outfile=$datadir/${app}.yaml
    echo "Writing: $outfile"
    $SITE/manage.py dumpdata --format=yaml --indent=4 --output=$outfile $app
done

echo "Syncing $datadir to ${mirrdir}"
rsync -avz $datadir/ ${mirrdir}/
