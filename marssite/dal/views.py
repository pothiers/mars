import datetime
import json
import xml.etree.ElementTree as ET
from collections import OrderedDict

from django.db import connections
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

from siap.models import Image, VoiSiap
from tada.models import FilePrefix


dal_version = '0.1.6' # MVP. mostly untested

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
    proctype,
    filter,
    filesize,
    filename,
    dtacqnam as original_filename,  -- original_filename
    md5sum,
    exposure,
    obstype as observation_type,    -- observation_type
    obsmode as observation_mode,    -- observation_mode
    prodtype as product,            -- product ???
    proctype,    
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


def remove_leading(thestring, lead):
    """Remove LEAD from left of THESTRING if its there."""
    if thestring.startswith(lead):
        return thestring[len(lead):]
    return thestring

def db_float_range(range_value, field):
    """range_value:: [minVal, maxVal, bounds] 
    see: https://www.postgresql.org/docs/9.3/static/functions-range.html
    """
    if isinstance(range_value, list):
        # contains element (postresql SQL)
        # '[2011-01-01,2011-03-01)'::tsrange @> '2011-01-10'::timestamp
        # If the third argument is omitted, '[)' is assumed.
        #
        # INclusive bound :: "(", ")"
        # EXclusive bound :: "[", "]"
        minval,maxval,*xtra = range_value
        bounds = xtra[0] if (len(xtra) > 0) else '[)'
        clause = (" AND ('{}{},{}{}'::numrange @> {})"
                  .format(bounds[0], minval, maxval, bounds[1], field))
    else:
        clause = " AND ({} = '{}')".format(field, range_value)
    return clause

def db_time_range(range_value, field):
    # Edge case bugs!!!
    if isinstance(range_value, list):
        # contains element (postresql SQL)
        # '[2011-01-01,2011-03-01)'::tsrange @> '2011-01-10'::timestamp
        # If the third argument is omitted, '[)' is assumed.
        #
        # INclusive bound :: "(", ")"
        # EXclusive bound :: "[", "]"
        mindate,maxdate,*xtra = range_value
        bounds = xtra[0] if (len(xtra) > 0) else '[)'
        clause = (" AND ('{}{},{}{}'::tsrange @> {}::timestamp)"
                  .format(bounds[0], mindate, maxdate, bounds[1], field))
    else:
        clause = " AND ({} = '{}')".format(field, range_value)
    return clause

def db_exact(value, field):
    clause = " AND ({} = '{}')".format(field, value)
    return clause

def db_oneof(value_list, field):
    clause = ""
    for val in value_list:
        clause += " OR ({} = '{}')".format(field, val)
    return ' AND (' + remove_leading(clause, ' OR ') + ')'

proc_LUT = dict(raw = 'raw',
                calibrated = 'InstCal',
                reprojected = 'projected',
                stacked = 'stacked',
                master_calibration = 'mastercal',
                image_tiles = 'tiled',
                sky_subtracted = 'skysub')
               

## Under PSQL, copy SELECTed results to CSV using:
#
# \copy (SELECT * from voi.siap WHERE (ra <= 186.368791666667) AND (ra >= 176.368791666667) AND (dec <= -40.5396111111111) AND (dec >= -50.5396111111111) AND (dtpi = 'Cypriano') AND (dtpropid = 'noao') AND ('[2009-04-01,2009-04-03]'::tsrange @> date_obs::timestamp) AND (dtacqnam = '/ua84/mosaic/tflagana/3103/stdr1_012.fits') AND ((telescope = 'ct4m') OR (telescope = 'foobar')) AND ((instrument = 'mosaic_2')) AND (release_date = '2010-10-01T00:00:00') AND ((proctype = 'raw') OR (proctype = 'InstCal')) AND (exposure = '15')) TO '~/data/metadata-dal-2.csv'

# curl -H "Content-Type: application/json" -X POST -d @fixtures/search-sample.json http://localhost:8000/dal/search/ > ~/response.json
# curl -H "Content-Type: application/json" -X POST -d @request.json http://localhost:8000/dal/search/ | python -m json.tool
@csrf_exempt
def search_by_json(request):
    # !!! Verify values (e.g. telescope) are valid. Avoid SQL injection hit.
    page_limit = int(request.GET.get('limit','100')) # num of records per page
    limit_clause = 'LIMIT {}'.format(page_limit)
    page = int(request.GET.get('page','1'))
    offset = (page-1) * page_limit
    offset_clause = 'OFFSET {}'.format(offset)
    # order:: comma delimitied, leading +/-  (ascending/descending)
    order_fields = request.GET.get('order','+reference')
    order_clause = ('ORDER BY ' +
                    ', '.join(['{} {}'.format(f[1:], ('DESC'
                                                      if f[0]=='-' else 'DESC'))
                               for f in order_fields.split()]))
    print('EXECUTING: views<dal>:search_by_file; method={}, content_type={}'
          .format(request.method, request.content_type))
    if request.method == 'POST':
        root = ET.Element('search')
        #!print('DBG body str={}'.format(request.body.decode('utf-8')))
        if request.content_type == "application/json":
            body = json.loads(request.body.decode('utf-8'))
            jsearch = body['search']
            #print('jsearch={}'.format(jsearch))
            for k,v in jsearch.items():
                e = ET.SubElement(root, k)
                if isinstance(v, dict):
                    for k2,v2 in v.items():                 
                        ET.SubElement(e, k2).text = str(v2)
                else:
                    e.text = str(v)
            #print('root={}'.format(root))
            tree = ET.ElementTree(root)
            xmlstr = ET.tostring(root)
            #print('xml search={}'.format(xmlstr))
            search_by_xmlstr(xmlstr)
        elif request.content_type == "application/xml":
            pass

        # Query Legacy Science Archive
        cursor = connections['archive'].cursor()
        # Force material view refresh
        #!cursor.execute('SELECT * FROM refresh_voi_material_views()')
        where = '' # WHERE clause innards
        
        slop = jsearch.get('search_box_min', .001)
        if 'coordinates' in jsearch:
            coord = jsearch['coordinates']
            where += ((' AND (ra <= {}) AND (ra >= {})'
                      ' AND (dec <= {}) AND (dec >= {})')
                      .format(coord['ra'] + slop,
                              coord['ra'] - slop,
                              coord['dec'] + slop,
                              coord['dec'] - slop))
        if 'pi' in jsearch:
            where += db_exact(jsearch['pi'], 'dtpi')
        if 'prop_id' in jsearch:
            #where += "(dtpropid = '{}')".format(jsearch['prop_id'])
            where += db_exact(jsearch['prop_id'], 'dtpropid')
        if 'obs_date' in jsearch:
            where += db_time_range(jsearch['obs_date'], 'date_obs')
        if 'filename' in jsearch: 
            where += db_exact(jsearch['filename'], 'dtnsanam')
        if 'original_filename' in jsearch: 
            where += db_exact(jsearch['original_filename'], 'dtacqnam')
        if 'telescope' in jsearch:
            where += db_oneof(jsearch['telescope'], 'telescope')
        if 'instrument' in jsearch: 
            where += db_oneof(jsearch['instrument'], 'instrument')
        if 'release_date' in jsearch: 
            where += db_time_range(jsearch['release_date'], 'release_date')
        if 'flag_raw' in jsearch:
            where += db_exact(jsearch['flag_raw'], 'rawfile')
        if 'image_filter' in jsearch:
            where += db_oneof([proc_LUT[p] for p in jsearch['image_filter']],
                               'proctype')
        if 'exposure_time' in jsearch:
            where += db_float_range(jsearch['exposure_time'], 'exposure')

        where = remove_leading(where, ' AND ')
        #print('DBG-2 where="{}"'.format(where))
        where_clause = '' if len(where) == 0 else 'WHERE {}'.format(where)
        sql0 = 'SELECT count(reference) FROM voi.siap {}'.format(where_clause)
        cursor.execute(sql0)
        total_count = cursor.fetchone()[0]
        sql = ('SELECT {} FROM voi.siap {} {} {} {}'
               .format(response_fields,
                       where_clause,
                       order_clause,
                       limit_clause,
                       offset_clause  ))
        print('DBG-2 sql={}'.format(sql))
        cursor.execute(sql)
        results = dictfetchall(cursor)
        #print('DBG results={}'.format(results))
        meta = OrderedDict.fromkeys(['dal_version', 'timestamp',
                                     'comment', 'sql',
                                     'page_result_count',
                                     'to_here_count',
                                     'total_count'])
        meta.update(
            dal_version = dal_version,
            timestamp = datetime.datetime.now(),
            comment = (
                'WARNING: Little testing.'
                ' Does not use "image_filter".'
            ),
            sql = sql,
            page_result_count = len(results),
            to_here_count = offset + len(results),
            total_count = total_count,
        )
        resp = OrderedDict.fromkeys(['meta','resultset'])
        resp.update( meta = meta, resultset = results)
        return JsonResponse(resp)
    elif request.method == 'GET':
        return HttpResponse('Requires POST with json payload')
    

@csrf_exempt
def tele_inst_pairs(request):
    """
    Retrieve all valid telescope/instrument pairs. 
    Determined by TADA file prefix table.
    """
    qs = FilePrefix.objects.all().order_by('pk').values('telescope',
                                                        'instrument')
    return JsonResponse([(d['telescope'],d['instrument']) for d in list(qs)],
                         safe=False)
