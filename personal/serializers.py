from rest_framework import serializers
from .models import *


class OperatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operator
        fields = '__all__'
        read_only_fields = ('id', 'updated_at', 'created_at')


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = '__all__'
        read_only_fields = ('id', 'created_at')


class PrinterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Printer
        fields = '__all__'
        read_only_fields = ('id', 'updated_at', 'created_at')


class WorkstationSerializer(serializers.ModelSerializer):
    printers = PrinterSerializer(required=False, many=True)

    class Meta:
        model = Workstation
        fields = '__all__'
        read_only_fields = ('id', 'updated_at', 'created_at')
