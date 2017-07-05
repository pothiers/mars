# Example:
# ./manage.py test --settings=marssite.test_settings dal.tests
# TO ADD:
#  - verify EXISTANCE of "meta" fields: dal_version, timestamp, comment, sql
#         'page_result_count', 'to_here_count', 'total_count'


from django.core.urlresolvers import reverse
from django.test import TestCase, Client, RequestFactory
import dal.views
from marssite import settings
import json
from . import expected as exp



class SearchTest(TestCase):
    def test_search_0(self):
        "No filter. Verify: API version."
        req = '{ "search" : { } }'
        #print('DBG: Using archive database: {}'.format(settings.DATABASES['archive']['HOST']))
        response = self.client.post('/dal/search/',
                                    content_type='application/json',
                                    data=req  )
        print('DBG: response={}'.format(response.content.decode()))
        self.assertEqual(json.dumps(response.json()['meta']['dal_version']),
                         '"0.1.6"',
                         msg='Unexpected API version')

    def test_search_1(self):
        "MVP-1. Basics. No validation of input"
        req = '''{ "search":{
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
        
        response = self.client.post('/dal/search/',
                                    content_type='application/json',
                                    data=req  )
        #!print('DBG: response={}'.format(response.content.decode()))
        self.assertJSONEqual(json.dumps(response.json()['resultset']),
                             json.dumps(json.loads(exp.search_1)['resultset']),
                             msg='Unexpected resultset')

