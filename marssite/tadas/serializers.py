from rest_framework import serializers
from .models import Submittal


class SubmittalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submittal
