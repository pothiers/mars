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


