from django.test import TestCase, RequestFactory
from django.test import Client

from .models import VoiSiap
import siap.views

#!class SiapTest(TestCase):
#!    # Load (special test) DB with data
#!
#!    # (Hard to do this with our Archive DB!)
#!    fixtures = ['test.json']
#!
#!    def setUp(self):
#!        self.factory = RequestFactory()
#!
#!    def test_query_by_sql(self):
#!        sql="SELECT reference,dtacqnam FROM voi.siap WHERE reference LIKE '%TADA%' LIMIT 100;"
#!        print('DBG-0: sql={}'.format(sql))
#!        
#!        #! request = self.factory.get('/siap/squery')
#!        #! response = siap.views.query_by_sql(request)
#!        c = Client()
#!        response = c.post('/siap/squery', content_type='application/json', data=sql)
#!        print('DBG-1: response={}'.format(response))
