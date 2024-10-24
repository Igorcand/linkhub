from rest_framework import serializers

class SetField(serializers.ListField):
    def to_internal_value(self, data):
        return set(super().to_internal_value(data))
    
    def to_representation(self, data):
        return list(super().to_representation(data))

class PostResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    user_id = serializers.UUIDField() 
    title = serializers.CharField()
    body = serializers.CharField()
    links = SetField(child=serializers.UUIDField())


class CreatePostRequestSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255, allow_blank=False)
    body = serializers.CharField(max_length=255, allow_blank=True)
    room_id = serializers.UUIDField()
    links = SetField(child=serializers.UUIDField())

class CreatePostResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()

class DeletePostRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()

class ListPostResponseSerializer(serializers.Serializer):
    data = PostResponseSerializer(many=True)

class UpdatePartialPostRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    title = serializers.CharField(required=False)
    body = serializers.CharField(required=False)
    links = SetField(child=serializers.UUIDField(), required=False)