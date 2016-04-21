from rest_framework import serializers
from .models import Submittal, SourceFile


class SubmittalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submittal

class SourceFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SourceFile
        
        
