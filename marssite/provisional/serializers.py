from rest_framework import serializers
from .models import Fitsname


class FitsnameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Fitsname
        #fields = ('id','source')

    
#!class FitsnameSerializer(serializers.Serializer):
#!    pk = serializers.CharField(read_only=True, max_length=80)
#!    source = serializers.CharField(read_only=True, max_length=256)
#!
#!    def create(self, validated_data):
#!        """
#!        Create and return a new `Fitsname` instance, given the validated data.
#!        """
#!        return Fitsname.objects.create(**validated_data)
#!
#!    def update(self, instance, validated_data):
#!        """
#!        Update and return an existing `Fitsname` instance, given the validated data.
#!        """
#!        instance.source = validated_data.get('source', instance.source)
#!        instance.save()
#!        return instance
#!
