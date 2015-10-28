from rest_framework import serializers
from .models import Slot


class SlotSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Slot

