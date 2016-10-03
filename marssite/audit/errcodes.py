"""Transform error messages from dataq, tada, archive into something
suitable for AUDIT.
"""

import re
import logging


existsRE = re.compile(r"has already been stored in the database")
'''Failure reason:Failed to ingest
file:/noao-tuc-z1/tada/vagrant/5/k4n_20141114_122626_oru.hdr error
msg:Header for k4n_20141114_122626_oru.fits has already been stored in
the database'''

dup_propRE = re.compile(r"Could not find unique proposal")
'''Failure reason:Failed to ingest
file:/noao-tuc-z1/tada/vagrant/23/ksb_041016_195304_uuu_1188439357.hdr
error msg:Could not find unique proposal TEST-noao in metadata
database, found 0'''


dup_obspropRE = re.compile(r"Got more than one observation matching calibration date for proposal")
'''Failure reason:Failed to ingest
file:/noao-tuc-z1/tada/vagrant/2/k4k_140922_234549_zuu_1186823651.hdr
error msg:Got more than one observation matching calibration date for
proposal. Query: select distinct o from ObservationEntity o join fetch
o.proposalSet p where p.proposalId = ?1 and o.calibrationDate between
?2 and ?3 and o.publicDataReleaseDate < ?4'''

hdr_existsRE = re.compile(r"iRODS HDR file already exists at")
'''iRODS HDR file already exists at
/noao-tuc-z1/mtn/20160608/ct4m/NA/c4ai_160609_151943_ori.hdr on submit
of
/data1/tada/dropbox/20160609/ct4m-arcoiris/SPEC_FFtest0583.fits. Aborting
attempt to ingest.'''

prop_not_foundRE = re.compile(r"Could not find the proposal:")
'''Could not find the proposal:[NA] in the database.'''

nonfitsRE = re.compile(r"Cannot ingest non-FITS file:")
'''Cannot ingest non-FITS file:
/sandbox/tada/tests/smoke/tada-test-data/basic/uofa-mandle.jpg'''

missingreqRE = re.compile(r"header is missing required metadata fields")
'''Modified FITS header is missing required metadata fields (PROCTYPE, PRODTYPE) in file /sandbox/tada/tests/smoke/tada-test-data/basic/kptest.fits'''

baddateRE = re.compile(r"Could not parse DATE-OBS field")
'''Could not parse DATE-OBS field (2004-12-16) in header of: /sandbox/tada/tests/smoke/tada-test-data/basic/kp109391.fits.fz'''

stilutRE = re.compile(r"Unknown combination for stiLUT:")
'''Unknown combination for stiLUT: SITE(ct), TELESCOPE(ct09m), and
INSTRUMENT(biw) (in /var/tada/cache/20160616/ct09m-biw/f177.fits.fz)'''

fitsverifyRE = re.compile(r"Verify failed:")
'''Verify failed: /usr/local/bin/fitsverify -e -q /var/tada/cache/20110101/wiyn-bench/24dec_2014.061.fits.fz'''

notschedRE = re.compile(r"not in scheduled list of Propids")
''' Propid from hdr (BADSCRUB.BAD-PROPID) not in scheduled list of Propids ['2016A-0189', '2016A-0453']'''

etlkeyRE = re.compile(r"ETL failed to parse bad keyword value")
'''ETL failed to parse bad keyword value. keyword:[ZD] value:[30:26:47.67728784] Storing null value for keyword instead. ETL exception msg was: For input string: "30:26:47.67728784"'''

# these must be searched in order. First MatchFunc to return True wins.
ERRMAP = [
    # ERRCODE,  MatchREGEX,       ShortDesc
    ('DUPFITS', existsRE,         'Already stored in Archive'),
    ('BADPROP', dup_propRE,       'Unique propid not found' ),
    ('COLLIDE', dup_obspropRE,    'Multi-files match date + propid'),
    ('NOPROP',  prop_not_foundRE, 'Propid not in Archive DB'),
    ('MISSREQ', missingreqRE,     'Missing required metadata'),
    ('BADDATE', baddateRE,        'DATE-OBS bad format'),
    ('NOTFITS', nonfitsRE,        'Cannot ingest non-FITS file'),
    ('STILUT',  stilutRE,         'Prefix table missing entry'),
    ('NOVERIFY',fitsverifyRE,     'File fails fitsverify'),
    ('NOSCHED', notschedRE,       'Header propid not in schedule split list'),
    ('ETLKEY',  etlkeyRE,         'ETL cannot parse keyword. Subsititing'),
]

def errcode(detailed_error_message):
    ecode = ''

    if detailed_error_message == '':
        return ''

    for name, regex, desc in ERRMAP:
        if regex.search(detailed_error_message):
            ecode = name
            break
    if ecode == '':
        logging.error('errcode cannot code for error message: {}'
                      .format(detailed_error_message))
    return ecode
