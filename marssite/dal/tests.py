# Example:
# ./manage.py test --settings=marssite.test_settings tada.tests

from django.core.urlresolvers import reverse
from django.test import TestCase, Client, RequestFactory
import dal.views
from marssite import settings
import json

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
        
        expected_rs = '''[
    {
      "observation_mode": "imaging",
      "reference": "tu006122.fits.gz",
      "ra": "181.368083333333",
      "dec": "-45.5388055555556",
      "prop_id": "noao",
      "original_filename": "\/ua84\/mosaic\/tflagana\/3103\/stdr1_012.fits",
      "filename": null,
      "release_date": "2010-10-01T00:00:00",
      "filesize": 14234056,
      "observation_type": "object",
      "survey_id": null,
      "seeing": "0.9",
      "flag_raw": "stdr1_012",
      "exposure": "15",
      "depth": "23.04",
      "product": "png",
      "filter": "R Harris c6004",
      "instrument": "mosaic_2",
      "pi": "Cypriano",
      "telescope": "ct4m",
      "md5sum": null,
      "obs_date": "2009-04-01T01:23:27.900",
      "proctype": "InstCal"
    },
    {
      "observation_mode": "imaging",
      "reference": "tu006121.fits.gz",
      "ra": "181.368083333333",
      "dec": "-45.5388055555556",
      "prop_id": "noao",
      "original_filename": "\/ua84\/mosaic\/tflagana\/3103\/stdr1_012.fits",
      "filename": null,
      "release_date": "2010-10-01T00:00:00",
      "filesize": 96811,
      "observation_type": "object",
      "survey_id": null,
      "seeing": "0.9",
      "flag_raw": "stdr1_012",
      "exposure": "15",
      "depth": "23.04",
      "product": "dqmask",
      "filter": "R Harris c6004",
      "instrument": "mosaic_2",
      "pi": "Cypriano",
      "telescope": "ct4m",
      "md5sum": null,
      "obs_date": "2009-04-01T01:23:27.900",
      "proctype": "InstCal"
    },
    {
      "observation_mode": "imaging",
      "reference": "tu006120.fits.gz",
      "ra": "181.368083333333",
      "dec": "-45.5388055555556",
      "prop_id": "noao",
      "original_filename": "\/ua84\/mosaic\/tflagana\/3103\/stdr1_012.fits",
      "filename": null,
      "release_date": "2010-10-01T00:00:00",
      "filesize": 222411172,
      "observation_type": "object",
      "survey_id": null,
      "seeing": "0.9",
      "flag_raw": "stdr1_012",
      "exposure": "15",
      "depth": "23.04",
      "product": "image",
      "filter": "R Harris c6004",
      "instrument": "mosaic_2",
      "pi": "Cypriano",
      "telescope": "ct4m",
      "md5sum": null,
      "obs_date": "2009-04-01T01:23:27.900",
      "proctype": "InstCal"
    },
    {
      "observation_mode": "imaging",
      "reference": "ct1922390.fits.gz",
      "ra": "181.357875",
      "dec": "-45.5320555555556",
      "prop_id": "noao",
      "original_filename": "\/ua84\/mosaic\/tflagana\/3103\/stdr1_012.fits",
      "filename": null,
      "release_date": "2010-10-01T00:00:00",
      "filesize": 63471160,
      "observation_type": "object",
      "survey_id": null,
      "seeing": null,
      "flag_raw": null,
      "exposure": "15",
      "depth": null,
      "product": null,
      "filter": "R Harris c6004",
      "instrument": "mosaic_2",
      "pi": "Cypriano",
      "telescope": "ct4m",
      "md5sum": null,
      "obs_date": "2009-04-01T01:23:27.900",
      "proctype": "Raw"
    }
  ]'''
        print('DBG: test_search_1')
        print('DBG: Using databases: {}'.format(settings.DATABASES))
        resp = self.client.post('/dal/search/',
                                content_type='application/json',
                                data=req  )
        #print('DBG: response={}'.format(resp.content))
        print('DBG: response={}'.format(resp.json()))
        self.assertJSONEqual(json.dumps(resp.json()['resultset']),
                             expected_rs,
                            msg='Unexpected resultset')

