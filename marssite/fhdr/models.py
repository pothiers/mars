"""Simple treatment of FITS header fields as columns for the common fields.
All other FITS fields (less common) go into MDATA.
"""
from django.contrib.postgres.fields import HStoreField
from django.db import models

#!    telescopes = ['kp09m', 'ct1m', 'kp21m', 'ct15m', 'ctlab', 'kp4m', 'ct09m',
#!                  'ct4m',  'bok23m', 'ct13m', 'wiyn', 'kp35m', 'soar', 'kpcf']
#!    instruments = ['ispi', 'spartan', 'wildfire', 'mop/ice', '90prime', 'hdi',
#!                   'falmingos', 'ice', 'bench', 'arcoiris', 'goodman',
#!                   'echelle', 'spartan ir camera', 'decam', 'arcon',
#!                   'minimo/ice', 'chiron', 'y4kcam', 'kosmos', 'mosaic3',
#!                   'newfirm', 'whirc', 'osiris', 'sam', 'cosmos', 'soi',
#!                   'andicam', 'goodman spectrograph', 'gtcam', 'flamingos',
#!                   'mosaic', '(p)odi']

class FitsMetadata(models.Model):
    # THESE ONLY GET UPDATED when django is started.
    telescopes = [obj.name for obj in Telescope.objects.all()]
    instruments = [obj.name for obj in Instrument.objects.all()]


    # id       = models.AutoField(primary_key=True)  # this happens by default
    mdata      = HStoreField()

    instrument = models.CharField(max_length=40,
                                  choices=[(v, v.upper())
                                           for v in instruments] )
    telescope  = models.CharField(max_length=20,
                                  choices=[(v, v.upper())
                                           for v in telescopes] )
    prop_id    = models.CharField(max_length=20)
    date_obs   = models.DateTimeField()
    filename   = models.CharField(max_length=80)    
    
    
    def __str__(self):
        return self.reference
