from rest_framework import serializers

from .models import *


class LocationSerializer(serializers.ModelSerializer):
    is_nonstop = serializers.BooleanField(default=True)

    class Meta:
        model = Location
        fields = '__all__'
        read_only_fields = ('id', 'updated_at', 'created_at')


class ClipSerializer(serializers.ModelSerializer):
    locations = LocationSerializer(required=False, many=True)

    class Meta:
        model = Clip
        fields = '__all__'
        read_only_fields = ('id', 'updated_at', 'created_at')
