from django.db import models

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
        
