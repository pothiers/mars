from django.db import models


# Will ultimately replace tada/file_naming.py:stiLUT{}
class FilePrefix(models.Model):
    "Archive filename prefix coded from Site, Telescope, Instrument"

    site = models.CharField(max_length=10, 
                            help_text='Site (mountain)')
    telescope = models.CharField(max_length=10, 
                                 help_text=('Name used in FITS header '
                                            '(field name TELES'))
    instrument = models.CharField(max_length=20, unique=True,
                                  help_text=('Name used in FITS header '
                                             '(field name INSTRUME)'))
    tacinst = models.CharField(max_length=20, unique=True,
                           help_text='Name used by Dave Bells TAC Schedule')

    prefix = models.CharField(max_length=4,
                              help_text='Prefix for Archive Filename')
    
