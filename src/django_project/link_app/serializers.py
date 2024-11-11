from rest_framework import serializers

class LinkResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    url = serializers.CharField(max_length=255)
    user_id = serializers.UUIDField()

class CreateLinkRequestSerializer(serializers.Serializer):
    url = serializers.CharField(max_length=255, allow_blank=False)

class CreateLinkResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()

class DeleteLinkResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()

class ListLinkResponseSerializer(serializers.Serializer):
    data = LinkResponseSerializer(many=True)