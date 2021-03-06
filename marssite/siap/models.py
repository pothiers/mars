from django.db import models


## import siap.models
## im = siap.models.Image.objects.raw('SELECT * FROM voi.siap LIMIT 3')[0]
## pprint(im.__dict__)

class Image(models.Model):
    reference = models.CharField(max_length=80, primary_key=True)
    prop_id = models.CharField(max_length=80)
    dtpropid = models.CharField(max_length=80)
    dtnsanam = models.CharField(max_length=80)
    dtacqnam = models.CharField(max_length=80)
    date_obs = models.DateTimeField()
    
    class Meta:
        managed = False
        db_table = 'voi.siap' # Simple Image Access Prototype


    
class VoiSiap(models.Model):
    reference        = models.CharField(max_length=80, primary_key=True)
    fits_extension   = models.IntegerField()
    object           = models.CharField(max_length=80)
    survey           = models.CharField(max_length=80)
    surveyid         = models.CharField(max_length=80)
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
    filesize         = models.BigIntegerField()
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
    release_date     = models.DateTimeField()
    noao_id          = models.CharField(max_length=80)
    vo_id            = models.CharField(max_length=80)
    airmass          = models.FloatField()
    astrmcat         = models.CharField(max_length=80)
    biasfil          = models.CharField(max_length=80)
    bunit            = models.CharField(max_length=80)
    dqmask           = models.CharField(max_length=80)
    darkfil          = models.CharField(max_length=80)
    date_obs         = models.DateTimeField()
    flatfil          = models.CharField(max_length=80)
    ds_ident         = models.CharField(max_length=80)
    dtnsanam         = models.CharField(max_length=80)
    dtacqnam         = models.CharField(max_length=80)
    dtobserv         = models.CharField(max_length=80)
    dtpi             = models.CharField(max_length=80)
    dtpiaffl         = models.CharField(max_length=80)
    dtpropid         = models.CharField(max_length=80)
    dtsite           = models.CharField(max_length=80)
    dttitle          = models.CharField(max_length=80)
    dtutc            = models.DateTimeField()
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
    fits_data_product_id = models.BigIntegerField()
    corn1dec         = models.IntegerField()
    corn2dec         = models.IntegerField()
    corn3dec         = models.IntegerField()
    corn4dec         = models.IntegerField()
    corn1ra          = models.IntegerField()
    corn2ra          = models.IntegerField()
    corn3ra          = models.IntegerField()
    corn4ra          = models.IntegerField()
    rspgrp           = models.CharField(max_length=80)
    rsptgrp          = models.CharField(max_length=80)
    reject           = models.CharField(max_length=80)
    seqid            = models.CharField(max_length=80)
    plqname          = models.CharField(max_length=80)
    pldname          = models.CharField(max_length=80)
    fk5coords        = models.CharField(max_length=80) # geometry(Point,100000) 

    def __str__(self):
        return self.reference


    class Meta:
        managed = False
        db_table = 'voi.siap' # Simple Image Access Prototype

        
