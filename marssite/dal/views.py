import datetime
import json
#import dicttoxml
import jsonschema
import xml.etree.ElementTree as ET
from collections import OrderedDict

from django.db import connections
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.defaults import bad_request
from django.core import serializers

from siap.models import Image, VoiSiap
from tada.models import FilePrefix

import coreapi
from rest_framework.decorators import api_view, renderer_classes
from rest_framework import response, schemas, renderers
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer

from .serializers import FilePrefixSerializer

from . import exceptions as dex


dal_version = '0.1.7' # MVP. mostly untested



#    object as object_name,          -- object_name
COMMENTED_response_fields = '''
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

response_fields = '''
    reference,
    ra,
    dec,
    prop_id,
    surveyid as survey_id,
    date_obs as obs_date,
    dtpi as pi,
    telescope,
    instrument,
    release_date,
    rawfile as flag_raw,
    proctype,
    filter,
    filesize,
    filename,
    dtacqnam as original_filename,
    md5sum,
    exposure,
    obstype as observation_type,
    obsmode as observation_mode,
    prodtype as product,
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

def db_ti_oneof(value_list):
    clause = ""
    frag = ""
    try:
        for telescope,instrument in value_list:
            clause += " OR ((telescope = '{}') AND (instrument = '{}'))" \
                       .format(telescope, instrument)
        frag = ' AND (' + remove_leading(clause, ' OR ') + ')'
    except Exception as err:
        raise dex.BadTIFormat(
            'search.telescope_instrument but be list of form: '
            '[["tele1", "instrum1"], ["t2","i2"]]')
    return frag

proc_LUT = dict(raw = 'raw',
                calibrated = 'InstCal',
                reprojected = 'projected',
                stacked = 'stacked',
                master_calibration = 'mastercal',
                image_tiles = 'tiled',
                sky_subtracted = 'skysub')


def fake_error_response(request, error_type):
    fake_err_types = ['bad_numeric',
                      'bad_search_json',
    ]
    if error_type == 'bad_numeric':
        raise dex.BadNumeric('Bad numeric value')
    elif error_type == 'bad_search_json':
        raise dex.BadSearchSyntax('Invalid JSON for search. Bad syntax.')
    else:
        raise dex.BadFakeError(
            'Unknown value ({}) for URL ERROR parameter. Allowed: {}'
            .format(error_type, ','.join(fake_err_types)))



## Under PSQL, copy SELECTed results to CSV using:
#
# \copy (SELECT * from voi.siap WHERE (ra <= 186.368791666667) AND (ra >= 176.368791666667) AND (dec <= -40.5396111111111) AND (dec >= -50.5396111111111) AND (dtpi = 'Cypriano') AND (dtpropid = 'noao') AND ('[2009-04-01,2009-04-03]'::tsrange @> date_obs::timestamp) AND (dtacqnam = '/ua84/mosaic/tflagana/3103/stdr1_012.fits') AND ((telescope = 'ct4m') OR (telescope = 'foobar')) AND ((instrument = 'mosaic_2')) AND (release_date = '2010-10-01T00:00:00') AND ((proctype = 'raw') OR (proctype = 'InstCal')) AND (exposure = '15')) TO '~/data/metadata-dal-2.csv'

# curl -H "Content-Type: application/json" -X POST -d @fixtures/search-sample.json http://localhost:8000/dal/search/ > ~/response.json
# curl -H "Content-Type: application/json" -X POST -d @request.json http://localhost:8000/dal/search/ | python -m json.tool
@csrf_exempt
def search_by_json(request):
    """
    Search the NOAO Archive, returns a list of image resource metadata
    """
    #!print('DBG-0: search_by_json')
    gen_error = request.GET.get('error',None)
    if gen_error != None:
        return fake_error_response(request, gen_error)


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
    #!print('EXECUTING: views<dal>:search_by_file; method={}, content_type={}'
    #!      .format(request.method, request.content_type))
    if request.method == 'POST':
        root = ET.Element('search')
        #!print('DBG body str={}'.format(request.body.decode('utf-8')))
        if request.content_type == "application/json":
            body = json.loads(request.body.decode('utf-8'))
            jsearch = body['search']
            #xml = dicttoxml.dicttoxml(body)
            #!validate_by_xmlstr(xmlstr)
            # Validate against schema
            try:
                schemafile = '/etc/mars/search-schema.json'
                with open(schemafile) as f:
                    schema = json.load(f)
                    jsonschema.validate(body, schema)
            except Exception as err:
                raise dex.BadSearchSyntax('JSON did not validate against /etc/mars/search-schema.json'
                                          '; {}'.format(err))

        elif request.content_type == "application/xml":
            print('WARNING: processing of XML payload not implemented!!!')
            raise dex.CannotProcessContentType('Cannot parse content type: application/xml')
        else:
            raise dex.CannotProcessContentType('Cannot parse content type: {}'
                                               .format(request.content_type))

        avail_fields = set([
            'search_box_min',
            'pi',
            'prop_id',
            'obs_date',
            'filename',
            'original_filename',
            'telescope_instrument',
            'release_date',
            'flag_raw',
            'image_filter',
            'exposure_time',
            'coordinates',
        ])
        used_fields = set(jsearch.keys())
        if not (avail_fields >= used_fields):
            unavail = used_fields - avail_fields
            #print('DBG: Extra fields ({}) in search'.format(unavail))
            raise dex.UnknownSearchField('Extra fields ({}) in search'.format(unavail))
        assert(avail_fields >= used_fields)

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
        #!if 'telescope' in jsearch:
        #!    where += db_oneof(jsearch['telescope'], 'telescope')
        #!if 'instrument' in jsearch:
        #!    where += db_oneof(jsearch['instrument'], 'instrument')
        # NEW api (0.1.7): "telescope_instrument":[["ct4m", "cosmos"], ["soar","osiris"]]
        if 'telescope_instrument' in jsearch:
            where += db_ti_oneof(jsearch['telescope_instrument'])
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
        #! print('DBG-6: search_by_json; sql0=',sql0)
        cursor.execute(sql0)
        total_count = cursor.fetchone()[0]
        sql = ('SELECT {} FROM voi.siap {} {} {} {}'
               .format(' '.join(response_fields.split()),
                       where_clause,
                       order_clause,
                       limit_clause,
                       offset_clause  ))
        #! print('DBG-2 sql={}'.format(sql))
        cursor.execute(sql)
        results = dictfetchall(cursor)
        #print('DBG results={}'.format(results))
        meta = OrderedDict.fromkeys(['dal_version',
                                     'timestamp',
                                     'comment',
                                     'sql',
                                     'page_result_count',
                                     'to_here_count',
                                     'total_count'])
        meta.update(
            dal_version = dal_version,
            timestamp = datetime.datetime.now(),
            comment = (
                'WARNING: Has not been tested much.'
                ' Does not use IMAGE_FILTER.'
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
def staging(request):
    query = ""
    # check if files exist
    query = json.loads(request.body.decode('utf-8'))
    request = request.get(reverse('get_associations'),
                                data=json.dumps({"search":query}),
                                content_type='application/json')
    res = search_by_json(request)
    return JsonResponse(res)

def fetchAllFiles(request):
    # query used to generate results is in post
    query = request.POST.get("query")
    page = request.GET.get("page", 1)
    # build API request
    # Only need filenames
    # all results
    host = request.get_host()
    host = settings.MACHINE_IP
    offset = (page-1)*100
    files = []
    request.body = json.dumps({"search":json.loads(query)})
    result = search_by_json(request)
    resultset = result['resultset']
    for n in resultset:
        # check if file exists
        files.append(n['reference'])
    return files


@csrf_exempt
@api_view(['GET'])
def tele_inst_pairs(request):
    """
    Retrieve all valid telescope/instrument pairs.
    Determined by TADA file prefix table.

    Response will be an array of **telescope**, **instrument** pairs

    `[ [\"telescope1\", \"instrument1\"], [\"telescope2\", \"instrument2\"] ]`
    """
    qs = FilePrefix.objects.all().order_by('pk').values('telescope',
                                                        'instrument')
    serialized = FilePrefixSerializer(qs, many=True)
    return JsonResponse([(d['telescope'],d['instrument']) for d in list(serialized.data)],
                         safe=False)



schema = coreapi.Document(
    title="Search API",
    url="http://localhost:8000",

    content={
        "search": coreapi.Link(
            url="/dal/search/",
            action = "post",
            fields = [
                coreapi.Field(
                    name="obs_date",
                    required=False,
                    location="form",
                    description="Single date or date range"
                ),
                coreapi.Field(
                    name="prop_id",
                    required=False,
                    location="form",
                    description="Prop ID to search for"
                ),
                coreapi.Field(
                    name="pi",
                    required=False,
                    location="form",
                    description="Principle Investigator"
                ),
                coreapi.Field(
                    name="filename",
                    required="false",
                    location="form",
                    description="Ingested archival filename"
                )
            ],
            description='''
            NOAO Search API

Requests need to be wrapped in a root `search` paramater

            {
              \"search\":{
                 \"obs_date\":\"2015-09-06\"
              }
            }
            '''
        )
    }
)

@api_view()
@renderer_classes([SwaggerUIRenderer, OpenAPIRenderer])
def schema_view(request):
    '''
      Search API
    '''
    #generator = schema.SchemaGenerator(title='Bookings API')
    #return Response(generator.get_schema())
    return response.Response(schema)
