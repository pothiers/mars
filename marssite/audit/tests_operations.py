from django.test import TestCase, Client

class AuditTest(TestCase):
    def setUp(self):
        self.client = Client()


    def test_checknight(self):
        md5sum = 'faux-md5sum'
        tag = 'archive'
        host = 'localhost'
        resp = self.client.get('/audit/notchecknight/')
        self.assertContains(resp, 'Faux Dmo Checknight Monitor')

    def test_agg(self):
        md5sum = 'faux-md5sum'
        tag = 'archive'
        host = 'localhost'
        resp = self.client.get('/audit/agg/')
        #print('response={}'.format(resp.content))
        self.assertContains(resp, 'Aggregated Error Counts')
        
        
