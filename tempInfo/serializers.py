from rest_framework import serializers
from .models import TempInfo

class TempInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TempInfo
        fields = '__all__'

    def create(self, validated_data):
        tempInfo = TempInfo.objects.create(**validated_data)
        return tempInfo
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep.pop('user', None)
        return rep