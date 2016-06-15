from django.db import models

class Instrument(models.Model):
    tac = models.CharField(max_length=20, unique=True,
                           help_text='Name used by Dave Bells TAC Schedule')
    fits = models.CharField(max_length=20, unique=True,
                            help_text='Name used in FITS header (field name INSTRUME)')

class Telescope(models.Model):
    fits = models.CharField(max_length=10, unique=True,
                            help_text=('Name used in FITS header '
                                       '(field name TELESCOP)'))

class FilePrefix(models.Model):
    "Archive filename prefix coded from Site, Telescope, Instrument"

    site = models.CharField(max_length=2, unique=True)
    telescope = models.CharField(max_length=10, unique=True,
                                 help_text=('Name used in FITS header '
                                            '(field name TELES'))
    
