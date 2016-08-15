from django.test import TestCase, Client
#from .models import AuditRecord

# python3 manage.py test audit.tests

class AuditTest(TestCase):
    def setUp(self):
        #self.factory = RequestFactory()
        self.client = Client()

    def test_dome(self):
        req =  '''{ "observations": [
            {
                "md5sum": "dc45a997e9c4e2b13a4518bbf24338ff",
                "obsday": "2016-08-05",
                "telescope": "kp4m",
                "instrument": "mosaic3",
                "dome_host": "mosaic3",
                "mountain_host": "mtnkp1.sdm.noao.edu",
                "srcpath": "/data4/observer/mos396217.fits"
            },
            {
                "md5sum": "1095128e0660fa8cfc6c7972936252f7",
                "obsday": "2016-08-05",
                "telescope": "kp4m",
                "instrument": "mosaic3",
                "dome_host": "mosaic3",
                "mountain_host": "mtnkp1.sdm.noao.edu",
                "srcpath": "/data4/observer/mos396218.fits"
            }
        ] }'''
        #print('input json={}'.format(req))
        resp = self.client.post('/audit/source/',
                                content_type='application/json',
                                data=req  )
        # response=b'<p>Added 2 audit records. 0 already existed (ignored request to add).</p>\n<ul></ul>'
        print('response={}'.format(resp.content))
        self.assertContains(resp, 'Added ',
                            msg_prefix=('Unexpected output from webservice'
                            ' intended for use by DOME'))


    def test_fstop(self):
        md5sum = 'faux-md5sum'
        tag = 'archive'
        host = 'localhost'
        resp = self.client.post('/audit/fstop/{}/{}/{}/'
                                .format(md5sum, tag, host))
        #print('response={}'.format(resp.content))
        self.assertContains(resp, 'Updated FSTOP;')
        
        
