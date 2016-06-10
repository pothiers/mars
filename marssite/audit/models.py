from django.db import models
from django.utils import timezone
from django.utils.html import format_html
from django.contrib.postgres.fields import HStoreField

#!class Submittal(models.Model):
#!    source = models.CharField(max_length=256,
#!                              help_text='Path of file as submitted')
#!    archive = models.CharField(max_length=80,
#!                               help_text='Basename of FITS file in Archive')
#!    status = models.TextField( blank=True,
#!                               help_text='From Archive HTTP response')
#!    metadata = models.TextField(blank=True,
#!                                help_text='As JSON')
#!    when = models.DateTimeField(auto_now_add=True,  help_text='When submitted')
#!
#!    def __str__(self):
#!        return ('{} -- {}({}): {}'
#!                .format(self.source,self.archive,self.metadata,self.status))
#! 
#!    class Meta:
#!        ordering = ('when',)
#!     




class SourceFile(models.Model):
    telescopes = ('aat,ct09m,ct13m,ct15m,ct1m,ct4m,gem_n,gem_s,gemn,gems,het,'
                  'keckI,keckII,kp09m,kp13m,kp21m,kp4m,kpcf,'
                  'magI,magII,mmt,soar,wiyn,unknown').split(',')
    instruments = ['90prime',  'ccd_imager', 'mosaic3',] + sorted([
        'mop/ice', 'arcon', 'spartan', 'decam',
        'falmingos', 'gtcam', 'wildfire', 'chiron',
        'osiris', 'arcoiris', 'andicam', 'echelle', 'flamingos',
        'sam', 'newfirm', 'goodman', 'y4kcam', 'minimo/ice', 'ice',
        'ispi', 'mosaic', 'goodman spectrograph', 'hdi', 'bench',
        'kosmos', 'spartan ir camera', 'soi', '(p)odi', 'whirc',
        'cosmos',  'unknown'])
    errcodes = ['DUPFITS', 'BADPROP', 'COLLIDE', 'NOPROP', 'MISSREQ',
                'BADDATE', 'NOFITS', 'UNKNOWN', 'none']

    md5sum = models.CharField(max_length=40, primary_key=True,
                              help_text='MD5SUM of FITS file')
    obsday = models.DateField(null=True, # allow no Dome info, only Submit
                              help_text='Observation Day')
    telescope = models.CharField(max_length=10, # default='unknown',
                                 choices=[(val,val) for val in telescopes] )
    instrument = models.CharField(max_length=25, # default='unknown',
                                 choices=[(val,val) for val in instruments] )
    srcpath    = models.CharField(max_length=256, 
                                  help_text='Path of file as submitted')

    recorded  = models.DateTimeField(default=timezone.now,
                                     help_text='When SourceFile recorded')

    ##### Field values added by TADA
    
    submitted = models.DateTimeField(null=True,
                                     help_text='When submitted to archive')
    success   = models.NullBooleanField(
        help_text=('Null until ingest attempted.'
                   'Then True iff Archive reported success on ingest'))
    archerr   = models.CharField(max_length=256, blank=True,
                                 help_text='Archive ingest error message')
    errcode   = models.CharField(max_length=8,
                                 default='none',
                                 choices=[(val,val) for val in errcodes],
                                 help_text='Error code for Archive Ingest')


    archfile  = models.CharField(max_length=80, blank=True,
                                 help_text='Basename of FITS file in Archive')
    metadata = HStoreField(null=True,
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
        return '{}-{}-{}: {}'.format(self.telescope,
                                     self.instrument,
                                     self.obsday,
                                     self.srcpath)
 
    class Meta:
        ordering = ('telescope','instrument','srcpath')
        
        
