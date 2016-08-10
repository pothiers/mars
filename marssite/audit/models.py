from django.db import models
from django.utils import timezone
from django.utils.html import format_html
from django.contrib.postgres.fields import HStoreField
#!from water.models import Telescope,Instrument




class AuditRecord(models.Model):
    telescopes = ('aat,ct09m,ct13m,ct15m,ct1m,ct4m,gem_n,gem_s,gemn,gems,het,'
                  'keckI,keckII,kp09m,kp13m,kp21m,kp4m,kpcf,'
                  'magI,magII,mmt,soar,wiyn,unknown').split(',')
    instruments = ['arcoiris', '90prime',  'mosaic3', 'ccd_imager'] + sorted([
        'mop/ice', 'arcon', 'spartan', 'decam',
        'falmingos', 'gtcam', 'wildfire', 'chiron',
        'osiris', 'andicam', 'echelle', 'flamingos',
        'sam', 'newfirm', 'goodman', 'y4kcam', 'minimo/ice', 'ice',
        'ispi', 'mosaic', 'goodman spectrograph', 'hdi', 'bench',
        'kosmos', 'spartan ir camera', 'soi', '(p)odi', 'whirc',
        'cosmos',  'unknown'])
    fstops = [
        'dome',
        'mountain:dropbox', 'mountain:queue',
        'mountain:cache', 'mountain:anticache`',
        'valley:dropbox',   'valley:queue',
        'valley:cache',   'valley:anticache',
        'archive']
    #telescopes = [obj.name for obj in Telescope.objects.all()]
    #instruments = [obj.name for obj in Instrument.objects.all()]
    errcodes = ['DUPFITS', 'BADPROP', 'COLLIDE', 'NOPROP', 'MISSREQ',
                'BADDATE', 'NOFITS', 'UNKNOWN', 'none']

    # Field values provided by DOME
    md5sum = models.CharField(max_length=40, primary_key=True, db_index=True,
                              help_text='MD5SUM of FITS file')
    obsday = models.DateField(null=True, # allow no Dome info, only Submit
                              help_text='Observation Day')
    telescope = models.CharField(max_length=10, # default='unknown',
                                 choices=[(val,val) for val in telescopes] )
    instrument = models.CharField(max_length=25, # default='unknown',
                                 choices=[(val,val) for val in instruments] )
    srcpath = models.CharField(max_length=256, 
                               help_text='Path of file as submitted')
    dome_host =  models.CharField(max_length=40, blank=True,
                                  help_text='Host name of Dome that created FITS')
    mountain_host =  models.CharField(max_length=40, blank=True,
                                 help_text='Host name of Mountain that received FITS')
    valley_host =  models.CharField(max_length=40, blank=True,
                                 help_text='Host name of Mountain that received FITS')
    
    # Field values automatically filled in (was called "recorded")
    updated  = models.DateTimeField(default=timezone.now,
                                     help_text='When AuditRecord updated')

    ##### Field values added by TADA

    fstop = models.CharField(max_length=25, blank=True,
                             choices=[(val,val) for val in fstops],
                             help_text = 'Most downstream stop of FITS file')
    
    submitted = models.DateTimeField(blank=True, null=True,
                                     help_text='When submitted to archive')
    success   = models.NullBooleanField(
        help_text=('Null until ingest attempted.'
                   'Then True iff Archive reported success on ingest'))
    archerr   = models.CharField(max_length=256, blank=True,
                                 help_text='Archive ingest error message')
    errcode   = models.CharField(max_length=10,
                                 default='none',
                                 choices=[(val,val) for val in errcodes],
                                 help_text='Error code for Archive Ingest')

    archfile  = models.CharField(max_length=80, blank=True,
                                 help_text='Basename of FITS file in Archive')
    metadata = HStoreField(blank=True, null=True,
                           help_text='FITS metadata changed by ingest')

    ##### Field values used for bookkeeping (by DART)
    staged   = models.BooleanField(
        default=False,
        help_text=('Marked for subsequent action.'))

    
    def narrow_srcpath(self):
        return format_html(
            '<span style="color: green; width: 10px;">{}</span>',
            self.srcpath,
        )
            
    def __str__(self):
        return '{}-{}'.format(self.obsday, self.instrument)

 
    #!class Meta:
    #!    ordering = ('telescope','instrument','srcpath')
        
        
