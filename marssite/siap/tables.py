import django_tables2 as tables
from django_tables2.utils import A  # alias for Accessor

class SiapTable(tables.Table):
    reference     = tables.TemplateColumn('<a href="http://nsaserver.sdm.noao.edu:7003/?fileRef={{record.reference}}">{{record.reference}}</a>')
    ra            = tables.Column()
    dec           = tables.Column()
    instrument    = tables.Column()
    telescope     = tables.Column()
    date_obs      = tables.DateColumn(short=True)
    dtacqnam      = tables.Column()
    dtpropid      = tables.Column()
    dtsite        = tables.Column()
    proctype      = tables.Column()
    prodtype      = tables.Column()
    start_date    = tables.DateColumn(short=True)
    release_date  = tables.DateColumn(short=True)
    
    class Meta:
        attrs = {'class': 'siap'}
