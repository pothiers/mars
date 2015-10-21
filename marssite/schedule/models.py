from django.db import models

class EmptySlot(models.Model):
    telescope = models.CharField(max_length=80)
    obsdate = models.DateField()

    class Meta:
        unique_together = ('telescope', 'obsdate')
        index_together = ['telescope', 'obsdate']

class Slot(models.Model):
    telescope = models.CharField(max_length=80)
    obsdate = models.DateField()
    propid = models.CharField(max_length=12)

    pi_name = models.CharField(max_length=80)
    pi_affiliation = models.CharField(max_length=160)
    title = models.CharField(max_length=256)

    frozen = models.BooleanField(default=False)

    class Meta:
        unique_together = ('telescope', 'obsdate')
        index_together = ['telescope', 'obsdate']
        


class SlotSet(models.Model):
    xmlfile = models.FileField(upload_to='mars/%Y%m%d/schedule.xml')
    begin = models.DateField()
    end = models.DateField()
