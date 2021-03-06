'''For eventual replacement of legacy Science Archive DB'''

# Add TacInstrumentAlias ??

from django.db import models


class Site(models.Model):
    name = models.CharField(max_length=10, primary_key=True,
                            help_text='Site (mountain)')
    def __str__(self): return self.name

class Telescope(models.Model):
    name = models.CharField(max_length=10, primary_key=True,
                            help_text=('Name used in FITS header '
                                       '(field name TELES'))
    def __str__(self): return self.name

class Instrument(models.Model):
    name = models.CharField(
        max_length=20, primary_key=True,
        help_text=('Name used in FITS header (field name INSTRUME)'))

    def __str__(self): return self.name


##############################################################################
### New schema (PROPOSED) to replace Legacy Science Archive 
###

class File(models.Model):
    id = models.CharField(max_length=32, primary_key=True) # md5sum of file as stored in MSS
    filesize         = models.BigIntegerField()
    release_date     = models.DateTimeField()

    
class Hdu(models.Model):
    hdu_index = models.IntegerField() # Primary HDU: hdu_index=0
    primary_hdu_id = models.ForeignKey('self', on_delete=models.CASCADE)
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    #! extra = HStoreField() # All HDR fields not otherwise stored.

    # Approximately from VoiSiap (Legacy Science Archive)
    object           = models.CharField(max_length=80)
    survey           = models.CharField(max_length=80)
    survey_id        = models.CharField(max_length=80) # was "surveyid"
    prop_id          = models.CharField(max_length=80)
    start_date       = models.DateTimeField()
    ra               = models.FloatField()
    dec              = models.FloatField()
    equinox          = models.FloatField()
    naxes            = models.IntegerField()
    naxis_length     = models.CharField(max_length=80)
    mimetype         = models.CharField(max_length=80)
    instrument       = models.CharField(max_length=80)
    telescope        = models.CharField(max_length=80)
    pixflags         = models.CharField(max_length=80)
    bandpass_id      = models.CharField(max_length=80)
    bandpass_unit    = models.CharField(max_length=80)
    bandpass_lolimit = models.CharField(max_length=80)
    bandpass_hilimit = models.CharField(max_length=80)
    exposure         = models.FloatField()
    depth            = models.FloatField()
    depth_err        = models.CharField(max_length=80)
    magzero          = models.FloatField()
    magerr           = models.FloatField()
    seeing           = models.FloatField()
    airmass          = models.FloatField()
    astrmcat         = models.CharField(max_length=80)
    biasfil          = models.CharField(max_length=80)
    bunit            = models.CharField(max_length=80)
    dqmask           = models.CharField(max_length=80)
    darkfil          = models.CharField(max_length=80)
    date_obs         = models.DateTimeField()
    flatfil          = models.CharField(max_length=80)
    ds_ident         = models.CharField(max_length=80)
    # dtnsanam         = models.CharField(max_length=80)
    # dtacqnam         = models.CharField(max_length=80)
    # dtobserv         = models.CharField(max_length=80)
    # dtpi             = models.CharField(max_length=80)
    # dtpiaffl         = models.CharField(max_length=80)
    # dtpropid         = models.CharField(max_length=80)
    # dtsite           = models.CharField(max_length=80)
    # dttitle          = models.CharField(max_length=80)
    # dtutc            = models.DateTimeField()
    efftime          = models.FloatField()
    filter           = models.CharField(max_length=80)
    filtid           = models.CharField(max_length=80)
    frngfil          = models.CharField(max_length=80)
    ha               = models.FloatField()
    instrume         = models.CharField(max_length=80)
    md5sum           = models.CharField(max_length=80)
    mjd_obs          = models.FloatField()
    obs_elev         = models.FloatField()
    obs_lat          = models.FloatField()
    obs_long         = models.FloatField()
    photbw           = models.FloatField()
    photclam         = models.FloatField()
    photfwhm         = models.FloatField()
    pipeline         = models.CharField(max_length=80)
    plver            = models.CharField(max_length=80)
    proctype         = models.CharField(max_length=80)
    prodtype         = models.CharField(max_length=80)
    puplfil          = models.CharField(max_length=80)
    radesys          = models.CharField(max_length=80)
    rawfile          = models.CharField(max_length=80)
    sb_recno         = models.IntegerField()
    sflatfil         = models.CharField(max_length=80)
    timesys          = models.CharField(max_length=80)
    disper           = models.CharField(max_length=80)
    obsmode          = models.CharField(max_length=80)
    filename         = models.CharField(max_length=80)
    nocslit          = models.CharField(max_length=80)
    nocssn           = models.CharField(max_length=80)
    zd               = models.FloatField()
    # fits_data_product_id = models.BigIntegerField()
    # Store corners (or polygon) in single field? !!!
    #! corn1dec         = models.IntegerField()
    #! corn2dec         = models.IntegerField()
    #! corn3dec         = models.IntegerField()
    #! corn4dec         = models.IntegerField()
    #! corn1ra          = models.IntegerField()
    #! corn2ra          = models.IntegerField()
    #! corn3ra          = models.IntegerField()
    #! corn4ra          = models.IntegerField()
    rspgrp           = models.CharField(max_length=80)
    rsptgrp          = models.CharField(max_length=80)
    reject           = models.CharField(max_length=80)
    seqid            = models.CharField(max_length=80)
    plqname          = models.CharField(max_length=80)
    pldname          = models.CharField(max_length=80)
    # FK5 is an equatorial coordinate system (coordinate system linked
    # to the Earth) based on its J2000 position.
    fk5coords        = models.CharField(max_length=80) # geometry(Point,100000) 

