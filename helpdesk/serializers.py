from rest_framework import serializers

from .models import *
from personal.serializers import OperatorSerializer, WorkstationSerializer


class ApplicationSerializer(serializers.ModelSerializer):
    operator = OperatorSerializer(required=False)
    workstation = WorkstationSerializer(required=False)
    executor = OperatorSerializer(required=False)
    signer = OperatorSerializer(required=False)

    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = ('id', 'updated_at', 'created_at')


class ButtonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Button
        fields = '__all__'
        read_only_fields = ('id', 'updated_at', 'created_at')
