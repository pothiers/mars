#!/bin/bash -e
# PURPOSE: Build RPM for MARS and copy to SDM repo
#

MIRRORS="sdmvm1.tuc.noao.edu"

marsdir="$HOME/sandbox/mars"
marsrpm="${marsdir}/dist/mars-*.noarch.rpm"

# Get new version number
pushd $marsdir > /dev/null
vers=`cat marssite/water/VERSION`
echo -n "Current version of MARS is $vers ; "
read -i "$vers" -p "What is the new version? " newvers rem
echo $newvers > marssite/VERSION
marsvers=$newvers
popd > /dev/null

pushd $marsdir > /dev/null
echo ""
echo "###"
echo "### Build MARS"
echo "###"
python3 setup.py build bdist --format rpm
popd > /dev/null

echo "###"
echo "### Copy RPMs to repo"
echo "###"
rsync -av $marsrpm  pothiers@$MIRRORS:/repo/mirrors/mars
ssh -t pothiers@$MIRRORS "createrepo /repo/mirrors/mars"

echo "### Versions copied to SDM repo:"
echo "MARS:  $marsvers"
