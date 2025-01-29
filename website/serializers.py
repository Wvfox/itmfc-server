from rest_framework import serializers

from .models import *


class VacancySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = '__all__'
        read_only_fields = ('id', 'created_at')
