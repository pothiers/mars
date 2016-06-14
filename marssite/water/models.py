from django.db import models

class Instrument(models.Model):
    tac = models.CharField(max_length=20, unique=True,
                           help_text='Name used by Dave Bells TAC Schedule')
    fits = models.CharField(max_length=20, unique=True,
                            help_text='Name used in FITS header (field name INSTRUME)')

class Telescope(models.Model):
    fits = models.CharField(max_length=10, unique=True,
                            help_text='Name used in FITS header (field name TELESCOP)')
    
    
