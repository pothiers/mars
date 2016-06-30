from django.core.urlresolvers import reverse

import django_tables2 as tables
from django_tables2.utils import A  # alias for Accessor

def latest_release(table):
    return max(x['release_date'].date() for x in table.data).isoformat()

class SiapTable(tables.Table):
    #reference     = tables.TemplateColumn('<a href="http://nsaserver.sdm.noao.edu:7003/?fileRef={{record.reference}}">{{record.reference}}</a>')
    reference     = tables.TemplateColumn(
        '<a href="{% url \'siap:retrieve_fits\' '
        'record.date_obs|date:"Y-m-d" record.telescope record.dtpropid record.reference%}">'
        '{{record.reference}}</a>')

    ra            = tables.Column()
    dec           = tables.Column()
    instrument    = tables.Column()
    telescope     = tables.Column()
    date_obs      = tables.DateColumn(short=True)
    dtacqnam      = tables.Column()
    dtpropid      = tables.Column(footer='Latest:')
    dtsite        = tables.Column()
    proctype      = tables.Column()
    prodtype      = tables.Column()
    start_date    = tables.DateColumn(short=True)
    release_date  = tables.DateColumn(short=True, footer=latest_release)

        
    class Meta:
        attrs = {'class': 'siap'}
        sequence = ('reference','date_obs','instrument','dtpropid', 'release_date',
                    'dtsite','telescope',
                    '...')
