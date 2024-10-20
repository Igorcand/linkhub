from rest_framework import serializers

class CreateRoomRequestSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, allow_blank=False)

class CreateRoomResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()