from rest_framework import serializers
from .models import Chat, Message, Profile
from django.contrib.auth.models import User


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["avatar"]


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ["__all__"]

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("profile", {})
        avatar = profile_data.get("avatar")

        instance = super().update(instance, validated_data)

        profile = instance.profile
        if avatar:
            profile.avatar = avatar
        profile.save()

        return instance


class MessageSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Message
        fields = ["__all__"]


class ChatSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    members = serializers.StringRelatedField(many=True)

    class Meta:
        model = Chat
        fields = ["__all__"]
