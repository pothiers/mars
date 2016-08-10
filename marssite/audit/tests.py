from django.test import TestCase, Client
#from .models import AuditRecord

# python3 manage.py test audit.tests

class AuditTest(TestCase):


    @classmethod
    def setUpClass(cls):
        #!super(AuditTest, cls).setUpClass()
        #!cls.client = Client()
        print('DOME setup')
        self.client = Client()

    def dome_test1(self):
        print('DOME test')
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
        print('input json={}'.format(req))
        resp = self.client.post('/audit/source/',
                                content_type='application/json',
                                data=req  )
        print('response={}'.format(resp.content))
        #self.assert
        
