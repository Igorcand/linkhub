from rest_framework import serializers

class RoomResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)
    user_id = serializers.UUIDField()


class CreateRoomRequestSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, allow_blank=False)

class CreateRoomResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()

class DeleteRoomRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()

class PartialUpdateRoomRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255, allow_blank=False)

class ListRoomResponseSerializer(serializers.Serializer):
    data = RoomResponseSerializer(many=True)