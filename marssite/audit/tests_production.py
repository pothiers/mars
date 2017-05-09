from django.test import TestCase, Client
#from .models import AuditRecord

# python3 manage.py test audit.tests

class AuditTest(TestCase):
    fixtures = ['natica.yaml', 'AuditRecord.dump.yaml']

    def setUp(self):
        #self.factory = RequestFactory()
        self.client = Client()

        
    def test_dome(self):
        "Create initial audit record(s).  Used in Domes."
        req =  '''{ "observations": [
            {
                "md5sum": "faux-checksum-0",
                "obsday": "2016-08-05",
                "telescope": "kp4m",
                "instrument": "mosaic3",
                "dome_host": "dome1",
                "srcpath": "/data4/observer/mos396217.fits"
            },
            {
                "md5sum": "faux-checksum-2",
                "obsday": "2016-08-05",
                "telescope": "kp4m",
                "instrument": "mosaic3",
                "dome_host": "dome1",
                "srcpath": "/data4/observer/mos396218.fits"
            }
        ] }'''
        #print('input json={}'.format(req))
        resp = self.client.post('/audit/source/',
                                content_type='application/json',
                                data=req  )
        # response=b'<p>Added 2 audit records. 0 already existed (ignored request to add).</p>\n<ul></ul>'
        #!print('DBG: response={}'.format(resp.content))
        self.assertContains(resp, 'SUCCESS: added',
                            msg_prefix=('Unexpected output from webservice'
                            ' intended for use by DOME'))


    def test_fstop(self):
        md5sum = 'faux-checksum-1'
        tag = 'archive'
        host = 'localhost'
        resp = self.client.post('/audit/fstop/{}/{}/{}/'
                                .format(md5sum, tag, host))
        #print('response={}'.format(resp.content))
        self.assertContains(resp, 'Updated FSTOP;')
