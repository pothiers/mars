import json
import xml.etree.ElementTree as ET


from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from siap.models import Image, VoiSiap
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

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




# curl -H "Content-Type: application/json" -X POST -d @fixtures/search-sample.json http://localhost:8000/dal/search/ > ~/response.html
@csrf_exempt
def search_by_json(request, limit=None):
    print('EXECUTING: views<dal>:search_by_file; method={}, content_type={}'
          .format(request.method, request.content_type))
    if request.method == 'POST':
        root = ET.Element('search')
        print('body str={}'.format(request.body.decode('utf-8')))
        if request.content_type == "application/json":
            body = json.loads(request.body.decode('utf-8'))
            #print('body={}'.format(body))
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
        elif request.content_type == "application/xml":
            pass

        #return JsonResponse(serializers.serialize(format, qs), safe=False)
        return JsonResponse(body, safe=False)
    elif request.method == 'GET':
        return HttpResponse('Requires POST with json payload')
    
