from rest_framework import serializers
from .models import RequestRecord

class RequestRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestRecord
        fields = '__all__'
