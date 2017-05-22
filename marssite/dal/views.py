import json

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

# cat <<EOF > search.json
# {"search": {
#     "coordinates": {"ra": "0", "dec": "0"},
#     "search_box_min": "0.2",
#     "instrument": ["kosmos", "cosmos"],
# } } 
# EOF
# curl -H "Content-Type: application/json" -X POST -d @search.json http://localhost:8000/dal/search/

@csrf_exempt
def search_by_json(request, limit=None):
    print('EXECUTING: views<dal>:search_by_file; method={}'
          .format(request.method))
    if request.method == 'POST':
        print('body str={}'.format(request.body.decode('utf-8')))
        body = json.loads(request.body.decode('utf-8'))
        print('body={}'.format(body))
        jsearch = body['search']

        #return JsonResponse(serializers.serialize(format, qs), safe=False)
        return JsonResponse(body, safe=False)
    elif request.method == 'GET':
        return HttpResponse('Requires POST with json payload')
    
