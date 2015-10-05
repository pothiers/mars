from django.db import models

# Create your models here.

class Fitsname(models.Model):
    dtnsanam = models.CharField(max_length=80,
                                 primary_key=True)
    dtacqnam = models.CharField(max_length=80)
    


