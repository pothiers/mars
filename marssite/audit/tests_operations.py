from django.test import TestCase, Client
from .models import AuditRecord

class AuditTest(TestCase):
    fixtures = ['AuditRecord.dump.yaml']
    
    def setUp(self):
        self.client = Client()
        # 2 successful ingests
        obj1 = AuditRecord.objects.get(pk='319fc6770dd33116622d2bba9722a5c5')
        obj2 = AuditRecord.objects.get(pk='3bc7e343b9cec6c32643663ce3612d5e')
        # 1 failed ingest
        obj3 = AuditRecord.objects.get(pk='d60aba3b0f2bdc1e6be4b107f6d884f8')
        
        obj1.staged = True
        obj2.staged = True
        obj3.staged = True
        obj1.save()
        obj2.save()
        obj3.save()


    def test_agg(self):
        resp = self.client.get('/audit/agg/')
        self.assertContains(resp, 'Aggregated Error Counts')

#!    def test_stagedarc(self):
#!        response = self.client.get('/audit/stagedarc/')
#!        expected = '/noao-tuc-z1/mtn/20160313/kp4m/2016A-0453/k4m_160314_072558_ori_tTADASMOKE.fits.fz /noao-tuc-z1/mtn/20161229/soar/soar/psg_161230_061637_ori_tTADASMOKE.fits.fz'
#!        self.assertEqual(200, response.status_code)
#!        self.assertHTMLEqual(response.content.decode(), expected)
#!
#!    def test_stagednoarc(self):
#!        response = self.client.get('/audit/stagednoarc/')
#!        expected = '/data/tada-test-data/short-drop/20160610/kp4m-mosaic3/mos3.badprop.fits'
#!        self.assertEqual(200, response.status_code)
#!        self.assertHTMLEqual(response.content.decode(), expected)
