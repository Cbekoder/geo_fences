from rest_framework import serializers

class LocationCheckSerializer(serializers.Serializer):
    device_id = serializers.CharField()
    lat = serializers.FloatField()
    lon = serializers.FloatField()