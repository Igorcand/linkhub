from rest_framework import serializers

class CreateUserRequestSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, allow_blank=False)
    username = serializers.CharField(max_length=150, allow_blank=False)
    email = serializers.EmailField(allow_blank=False)
    password = serializers.CharField(write_only=True, min_length=8)

class CreateUserResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class DeleteUserRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()

class UpdatePartialUserRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=False)
    username = serializers.CharField(max_length=30, allow_blank=False, required=True)