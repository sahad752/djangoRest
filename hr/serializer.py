from rest_framework import serializers
from hr.models import appointment

class AppointmentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    type = serializers.IntegerField()
    start_time = serializers.CharField(max_length=100)
    end_time = serializers.CharField(max_length=100)


    def create(self, validated_data):
        return appointment.objects.create(**validated_data)