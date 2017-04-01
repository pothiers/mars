#!/bin/bash
SCRIPT=$(readlink -e $0)     #Absolute path to this script
SCRIPTDIR=$(dirname $SCRIPT) #Absolute path this script is in

cd $SCRIPTDIR/marssite

# sometimes errors with 'NoneType' object is not iterable
# Stack track doesn't point to mars at all.
#!./manage.py test 

./manage.py test schedule.tests_production schedule.tests_operations tada.tests provisional.tests audit.tests_production audit.tests_operations

#./manage.py test schedule.tests_production
#./manage.py test schedule.tests_operations
#./manage.py test tada.tests
#
#./manage.py test provisional.tests
#./manage.py test audit.tests_production
#./manage.py test audit.tests_operations

#! ./manage.py test water.tests
#! ./manage.py test siap.tests

#! ./manage.py test tada.tests.TadaTest.test_table_prefix
