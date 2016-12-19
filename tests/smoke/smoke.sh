#!/bin/bash
# AUTHORS:    S. Pothier
# PURPOSE:    Wrapper for smoke test
# EXAMPLE:
#   loadenv lidar
#   $sb/lidar-matcher/test/smoke.sh
#

file=$0
dir=`dirname $file`
origdir=`pwd`
cd $dir

source smoke-lib.sh
return_code=0
SMOKEOUT="README-smoke-results.txt"


echo ""
echo "Starting tests in \"$dir\" ..."
echo ""
echo ""


#testOutput out tests.out '^\#' n
testCommand mars1_1 "./manage.py test 2>/dev/null" "^\#" y 1


###########################################
#! echo "WARNING: ignoring remainder of tests"
#! exit $return_code
###########################################


##############################################################################

rm $SMOKEOUT 2>/dev/null
if [ $return_code -eq 0 ]; then
  echo ""
  echo "ALL smoke tests PASSED ($SMOKEOUT created)"
  echo "All tests passed on " `date` > $SMOKEOUT
else
  echo "Smoke FAILED (no $SMOKEOUT produced)"
fi


# Don't move or remove! 
cd $origdir
exit $return_code

