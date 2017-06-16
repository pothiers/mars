from django.core.urlresolvers import reverse
from django.test import TestCase, Client, RequestFactory
import dal.views

class SearchTest(TestCase):
    def test_search_1(self):
        "MVP-1. Basics. No validation of input"

        req = '''{
    "search":{
        "coordinates": { 
            "ra": 181.368791666667,
            "dec": -45.5396111111111
        },
        "pi": "Cypriano",
        "search_box_min": 5.0,
        "prop_id": "noao",
        "obs_date": ["2009-04-01", "2009-04-03", "[]"],
        "TRY_FILENAME": "foo",
        "original_filename": "/ua84/mosaic/tflagana/3103/stdr1_012.fits",
        "telescope":["ct4m", "foobar"],
        "exposure_time": "15",
        "instrument":["mosaic_2"],
        "release_date": "2010-10-01T00:00:00",
        "image_filter":["raw", "calibrated"]
    }
}'''
        resp = self.client.post('/dal/search/',
                                content_type='application/json',
                                data=req  )
        #!print('DBG: response={}'.format(resp.content))
        self.assertContains(resp, 'SUCCESS: searched',
                            msg_prefix=('Unexpected output from webservice'
                                        ' intended for use by DOME'))

