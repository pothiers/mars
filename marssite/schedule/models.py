from django.db import models

class EmptySlot(models.Model):
    telescope = models.CharField(max_length=80)
    obsdate = models.DateField()

    class Meta:
        unique_together = ('telescope', 'obsdate')
        index_together = ['telescope', 'obsdate']

class Slot(models.Model):
    telescopes = ('ct09m,ct13m,ct15m,ct1m,ct4m,gem_n,gem_s,het,'
                  'keckI,keckII,kp09m,kp13m,kp21m,kp4m,kpcf,'
                  'magI,magII,mmt,soar,wiyn').split(',')
    
    telescope = models.CharField(max_length=80,
                                 choices=[(t,t) for t in telescopes] )
    obsdate = models.DateField(help_text='Observation date')
    propid = models.CharField(max_length=12,
                              help_text='YYYYs-nnnn (s:: A|B)')
    pi_name = models.CharField(max_length=80,
                               help_text='Principal Investigator name')
    pi_affiliation = models.CharField(max_length=160)
    title = models.CharField(max_length=256)

    frozen = models.BooleanField(default=False,
        help_text=('Protect against changing this slot '
                   'during a batch operation.'))
    class Meta:
        unique_together = ('telescope', 'obsdate')
        index_together = ['telescope', 'obsdate']
        


class SlotSet(models.Model):
    xmlfile = models.FileField(upload_to='mars/%Y%m%d/schedule.xml')
    begin = models.DateField()
    end = models.DateField()
