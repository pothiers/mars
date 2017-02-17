from django.db import models

class Site(models.Model):
    name = models.CharField(max_length=10, unique=True,
                            help_text='Site (mountain)')
    def __str__(self): return self.name

class Telescope(models.Model):
    name = models.CharField(max_length=10,  unique=True,
                            help_text=('Name used in FITS header '
                                       '(field name TELES'))
    def __str__(self): return self.name

class Instrument(models.Model):
    name = models.CharField(max_length=20, unique=True,
                            help_text=('Name used in FITS header '
                                       '(field name INSTRUME)'))
    def __str__(self): return self.name

class TacInstrument(models.Model):
    name = models.CharField(max_length=20, unique=True,
                            help_text='Name used by Dave Bells TAC Schedule')
    def __str__(self): return self.name

class InstrumentAlias(models.Model):
    reason = models.CharField(max_length=80)
    #!instrument = models.ForeignKey(Instrument)

# Will ultimately replace tada/file_naming.py:stiLUT{}
class FilePrefix(models.Model):
    "Archive filename prefix coded from Site, Telescope, Instrument"

    site = models.ForeignKey(Site)
    telescope = models.ForeignKey(Telescope)
    instrument = models.ForeignKey(Instrument)
    prefix = models.CharField(max_length=10,
                              help_text='Prefix for Archive Filename')
    comment = models.CharField(max_length=80, blank=True, default='')

class ObsType(models.Model):
    name = models.CharField(max_length=30, unique=True)
    code = models.CharField(max_length=1, unique=False)
    comment = models.CharField(max_length=80, blank=True, default='')

class ProcType(models.Model):
    name = models.CharField(max_length=30, unique=True)
    code = models.CharField(max_length=1, unique=False)
    comment = models.CharField(max_length=80, blank=True, default='')

class ProdType(models.Model):
    name = models.CharField(max_length=30, unique=True)
    code = models.CharField(max_length=1, unique=False)
    comment = models.CharField(max_length=80, blank=True, default='')


    
