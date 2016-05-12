from rest_framework import serializers
from .models import SourceFile



class SourceFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SourceFile
        
        
