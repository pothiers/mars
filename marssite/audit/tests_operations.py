from django.test import TestCase, Client

class AuditTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_agg(self):
        resp = self.client.get('/audit/agg/')
        self.assertContains(resp, 'Aggregated Error Counts')

#!    def test_stagedarc(self):
#!        resp = self.client.get('/audit/stagedarc/')
#!        self.assertContains(resp, 'no expected value available')
        
        
