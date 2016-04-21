from django.db import models
from django.utils import timezone

class Submittal(models.Model):
    source = models.CharField(max_length=256,
                              help_text='Path of file as submitted')
    archive = models.CharField(max_length=80,
                               help_text='Basename of FITS file in Archive')
    status = models.TextField( blank=True,
                               help_text='From Archive HTTP response')
    metadata = models.TextField(blank=True,
                                help_text='As JSON')
    when = models.DateTimeField(auto_now_add=True,  help_text='When submitted')

    def __str__(self):
        return ('{} -- {}({}): {}'
                .format(self.source,self.archive,self.metadata,self.status))
 
    class Meta:
        ordering = ('when',)
        

class SourceFile(models.Model):
    source    = models.CharField(max_length=256, primary_key=True,
                                  help_text='Path of file as submitted')
    recorded  = models.DateTimeField(default=timezone.now,
                                     help_text='When SourceFile recorded')
    submitted = models.DateTimeField(null=True,
                                     help_text='When submitted to archive')
    success   = models.NullBooleanField(
        help_text=('Null until ingest attempted.'
                   'Then True iff Archive reported success on ingest'))
    archerr   = models.CharField(max_length=256, blank=True,
                                 help_text='Archive ingest error message')
    archfile  = models.CharField(max_length=80, blank=True,
                                 help_text='Basename of FITS file in Archive')
    

    def __str__(self):
        return '{} -- {}'.format(self.recorded, self.source)
 
    class Meta:
        ordering = ('recorded',)
        
        
