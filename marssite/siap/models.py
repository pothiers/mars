from django.db import models

## import siap.models
## im = siap.models.Image.objects.raw('SELECT * FROM voi.siap LIMIT 3')[0]
## pprint(im.__dict__)

# Create your models here.
class Image(models.Model):
    reference = models.CharField(max_length=80,
                                 db_column='reference',
                                 primary_key=True)
    prop_id = models.CharField(max_length=80)
    dtpropid = models.CharField(max_length=80)
    dtnsanam = models.CharField(max_length=80)
    dtacqnam = models.CharField(max_length=80)
    
    class Meta:
        managed = False
        db_table = 'voi.siap' # Simple Image Access Prototype


