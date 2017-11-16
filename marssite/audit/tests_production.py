# ./manage.py test --keepdb audit.tests_production audit.tests_operations
# ./manage.py test --keepdb audit.tests_production.AuditTest.test_update_1
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


    def test_update_1(self):
        """Update audit successfully"""
        req =  '''
        {
        "telescope": "kp4m",
        "instrument": "mosaic3",
        "archerr": "Error (404) in MARS webservice call (http://mars.host:8000/schedule/dbpropid/kp4m/mosaic3/2016-08-18/2016A-0023/); Propid from hdr (2016A-0023) not in scheduled list of Propids ['2012B-0001']; Telescope=kp4m, Instrument=mosaic3, Date=2016-08-18.",
        "errcode": "NOSCHED",
        "updated": "2017-11-09T16:15:58.535067",
        "success": "False",
        "md5sum": "faux-checksum-NOT_IN_DB",
        "obsday": "2016-08-18",
        "srcpath": "/Data/Syncnight_Smoke/20160818/kp4m-mosaic3/mos397672.fits",
        "archfile": "",
        "metadata": {},
        "submitted": "2017-11-09T16:15:58.535067"
        }'''
        expected = '/audit/update/ DONE. created=True, obj=faux-checksum-NOT_IN_DB'
        resp = self.client.post('/audit/update/',
                                content_type='application/json',
                                data=req  )
        print('response={}'.format(resp.content))
        self.assertContains(resp, expected)
        
    def test_update_2(self):
        """Fail to update audit do to bad Request data"""
        req =  '''
        {
        "telescope": "kp4m",
        "instrument": "mosaic3",
        "archerr": "TOO-LONG.123456789.123456789.123456789.123456789.123456789.123456789.123456789.123456789.123456789.123456789.123456789.123456789.123456789.123456789.123456789.123456789.123456789.123456789.123456789.123456789.123456789.123456789.123456789.123456789.123456789.123456789",
        "errcode": "NOSCHED",
        "updated": "2017-11-09T16:15:58.535067",
        "success": "False",
        "md5sum": "faux-checksum-NOT_IN_DB",
        "obsday": "2016-08-18",
        "srcpath": "/home/mcmanus/Data/Syncnight_Smoke/20160818/kp4m-mosaic3/mos397672.fits",
        "archfile": "",
        "metadata": {},
        "submitted": "2017-11-09T16:15:58.535067"
        }'''
        expected = 'value too long for type character varying(256)\n'
        resp = self.client.post('/audit/update/',
                                content_type='application/json',
                                data=req  )
        print('response={}'.format(resp.content))
        self.assertContains(resp, expected, status_code=400)
