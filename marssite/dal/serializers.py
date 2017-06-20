from rest_framework import serializers
from siap.models import VoiSiap


class SiapSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VoiSiap
        fields = ('reference', 'prop_id', 'ra', 'dec',
                  'instrument', 'telescope', 'date_obs')



#class SearchSerializer(serializers.Serializer):
    
