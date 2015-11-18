from django.db import models

class EmptySlot(models.Model):
    telescope = models.CharField(max_length=80)
    obsdate = models.DateField()
    modified = models.DateTimeField(auto_now=True, help_text='When modified' )

    class Meta:
        unique_together = ('telescope', 'obsdate')
        index_together = ['telescope', 'obsdate']

class Proposal(models.Model):
    propid = models.CharField(primary_key=True,
                              max_length=12,
                              help_text='YYYYs-nnnn (s[emester]:: A|B)')
    title = models.CharField(max_length=256)
    pi_name = models.CharField(max_length=80,
                               help_text='Principal Investigator name')
    pi_affiliation = models.CharField(max_length=160)
    modified = models.DateTimeField(auto_now=True, help_text='When modified')
    
    def __str__(self):
        return self.propid
                
    
class Slot(models.Model):
    # These are the only telescopes allowed by the perl script that
    # uses a foreign web service for schedule retrieval.  Since the web
    # service will return error for anything else, we limit also.
    telescopes = ('ct09m,ct13m,ct15m,ct1m,ct4m,gem_n,gem_s,het,'
                  'keckI,keckII,kp09m,kp13m,kp21m,kp4m,kpcf,'
                  'magI,magII,mmt,soar,wiyn').split(',')

    telescope = models.CharField(max_length=10,
                                 choices=[(t,t) for t in telescopes] )
    obsdate = models.DateField(help_text='Observation date') # DATE-OBS
    proposals = models.ManyToManyField(Proposal)
    modified = models.DateTimeField(auto_now=True, help_text='When modified' )
    
    def propid_list(self):
        return ','.join([p.propid for p in self.proposals.all()[:4]])
    
    def __str__(self):
        return '{}:{}'.format(self.obsdate, self.telescope)
        
    #!pi_name = models.CharField(max_length=80,
    #!                           help_text='Principal Investigator name')
    #!pi_affiliation = models.CharField(max_length=160)
    #!title = models.CharField(max_length=256)
    #!
    #!frozen = models.BooleanField(default=False,
    #!    help_text=('Protect against changing this slot '
    #!               'during a batch operation.'))
    class Meta:
        unique_together = ('telescope', 'obsdate')
        index_together = ['telescope', 'obsdate']
        


class SlotSet(models.Model):
    xmlfile = models.FileField(upload_to='mars/%Y%m%d/schedule.xml')
    comment = models.CharField(max_length=256, blank=True)

