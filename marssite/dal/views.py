import json
import xml.etree.ElementTree as ET

from django.db import connections
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from siap.models import Image, VoiSiap
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

dal_version = '0.1.0' # MVP. mostly untested

search_spec_json = {
 "search":{
    "object_name" : "[text|optional]",
    "coordinates": { 
        "ra" : "[float|optional]",
        "dec": "[float|optional]"
    },
     "search_box_min": "[float|optional]",
     "prop_id":"[text|optional]",
     "obs_date":"[text|optional]",
     "filename":"[text|optional]",
     "telescope":"[array(text)|optional]",
     "instrument":"[array(text)|optional]",
     "release_date":"[date|optional]",
     "flag_raw":"[boolean|false]",
     "image_filter":{
         "calibrated" : "[boolean|false]",
         "reprojected" : "[boolean|false]",
         "stacked" : "[boolean|false]",
         "master_calibration" : "[boolean|false]",
         "image_tiles" : "[boolean|false]",
         "sky_subtracted" : "[boolean|false]",
     }
  }
}

response_spec_json = [
    {
        "object_name":"string",
        "ra": 0.0,
        "dec": 0.0,
        "prop_id":"string",
        "survey_id":"string",
        "obs_date":"2017-05-01",
        "pi":"string",
        "telescope":"string",
        "instrument":"string",
        "release_date":"2017-05-01",
        "flag_raw" : "bool",
        "image_type": "string(calibrated,stacked,etc)",
        "filter":"string",
        "file_size":0,
        "filename":"string",
        "original_filename":"string",
        "md5sum":"string",
        "exposure":0.0,
        "observation_type":"string",
        "observation_mode":"stirng",
        "product":"string",
        "seeing":"string",
        "depth":"string"
    }
]



#    object as object_name,          -- object_name
response_fields = '''
    reference,
    ra,
    dec,
    prop_id,
    surveyid as survey_id,          -- survey_id
    date_obs as obs_date,           -- obs_date
    dtpi as pi,                     -- pi
    telescope,
    instrument,
    release_date,
    rawfile as flag_raw,            -- flag_raw ???
    proctype as image_type,         -- image_type ???
    filter,
    filesize,
    filename,
    dtacqnam as original_filename,  -- original_filename
    md5sum,
    exposure,
    obstype as observation_type,    -- observation_type
    obsmode as observation_mode,    -- observation_mode
    prodtype as product,            -- product ???
    seeing,
    depth
'''

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

# ElementTree should be used only for TRUSTED sources (not directly) from web service.
def search_by_xmlstr(xmlstr):
    pass

    

# curl -H "Content-Type: application/json" -X POST -d @fixtures/search-sample.json http://localhost:8000/dal/search/ > ~/response.html
@csrf_exempt
def search_by_json(request):
    limit = request.GET.get('limit',99)
    print('EXECUTING: views<dal>:search_by_file; method={}, content_type={}'
          .format(request.method, request.content_type))
    if request.method == 'POST':
        root = ET.Element('search')
        print('body str={}'.format(request.body.decode('utf-8')))
        if request.content_type == "application/json":
            body = json.loads(request.body.decode('utf-8'))
            jsearch = body['search']
            print('jsearch={}'.format(jsearch))
            for k,v in jsearch.items():
                e = ET.SubElement(root, k)
                if isinstance(v, dict):
                    for k2,v2 in v.items():                 
                        ET.SubElement(e, k2).text = str(v2)
                else:
                    e.text = str(v)
            print('root={}'.format(root))
            tree = ET.ElementTree(root)
            xmlstr = ET.tostring(root)
            print('xml search={}'.format(xmlstr))
            search_by_xmlstr(xmlstr)
        elif request.content_type == "application/xml":
            pass

        # Query Legacy Science Archive
        cursor = connections['archive'].cursor()
        # Force material view refresh
        cursor.execute('SELECT * FROM refresh_voi_material_views()')
        where = '' # WHERE clause
        if 'coordinates' in jsearch:
            slop = .001
            coord = jsearch['coordinates']
            if len(where) > 0:  where += ' AND '
            where += ('(ra <= {}) AND (ra >= {}) AND (dec <= {}) AND (dec >= {})'
                      .format(coord['ra'] + slop,
                              coord['ra'] - slop,
                              coord['dec'] + slop,
                              coord['dec'] - slop))
            
        if 'telescope' in jsearch:
            if len(where) > 0:  where += ' AND '
            where += "((telescope = '{}')".format(jsearch['telescope'][0])
            for tele in jsearch['telescope'][1:]:
                where += " OR (telescope = '{}')".format(tele)
            where += ')'
        if 'instrument' in jsearch: 
            if len(where) > 0:  where += ' AND '
            where += "((instrument = '{}')".format(jsearch['instrument'][0])
            for inst in jsearch['instrument']:
                where += " OR (instrument = '{}')".format(inst)
            where += ')'
        if 'obs_date' in jsearch:
            if len(where) > 0:  where += ' AND '
            # Edge case bugs!!!
            if isinstance(jsearch['obs_date'], list):
                # contains element (postresql SQL)
                # '[2011-01-01,2011-03-01)'::tsrange @> '2011-01-10'::timestamp
                # If the third argument is omitted, '[)' is assumed.
                #
                # INclusive bound :: "(", ")"
                # EXclusive bound :: "[", "]"
                mindate,maxdate,*xtra = jsearch['obs_date']
                bounds = xtra[0] if (len(xtra) > 0) else '[)'
                where += ("('{}{},{}{}'::tsrange @> date_obs::timestamp)"
                          .format(bounds[0], mindate, maxdate, bounds[1]))
            else:
                obsdate = jsearch['obs_date']
                where += "(date_obs = '{}')".format(obsdate)

        sql = ('SELECT {} FROM voi.siap WHERE {} LIMIT {}'
               .format(response_fields, where, limit))
        print('DBG sql={}'.format(sql))
        cursor.execute(sql)
        results = dictfetchall(cursor)
        return JsonResponse(dict(resultset = results,
                                 meta = dict(dal_version = dal_version,
                                             comment = 'WARNING: Not tested',
                                             sql = sql,
                                 )))
    elif request.method == 'GET':
        return HttpResponse('Requires POST with json payload')
    
