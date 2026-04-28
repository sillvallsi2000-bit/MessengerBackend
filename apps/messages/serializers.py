from typing import Any, Dict

from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.serializers import ModelSerializer, ValidationError, Serializer
from .models import (
    MessagesTypeModel,
    MessageStatusModel,
    MessagesModel,
    MessageEditModel,
    MessageForwardModel,
    MessageHashtagModel,
    MessageLinkModel,
    MessageMetadataModel,
    MessageReactionModel,
    MessageReplaysModel,
)

from apps.user.models import UserModel
from apps.chats.models import ChatModel


from .models import MessagesTypeModel

from core.services.chat_service import get_or_create_chat
from apps.user.serializers import UserSerializer


class MessagesTypeSerializer(ModelSerializer):
    class Meta:
        model = MessagesTypeModel
        fields = (
            "name",
            "description",
            "code",
        )


class MessageStatusSerializer(ModelSerializer):
    class Meta:
        model = MessageStatusModel
        fields = (
            "message",
            "user",
            "status",
        )


class MessagesSerializer(ModelSerializer):
    target_id = serializers.SerializerMethodField()

    class Meta:
        model = MessagesModel
        fields = (
            "chat",
            "sender",
            "message_type",
            "message",
            "is_edited",
            "is_delited",
            "is_pined",
            "create_at",
            "update_at",
            "target_id",
        )

    def get_target_id(self, obj):
        request = self.context.get("request")
        if not request:
            return None
        chat = obj.chat
        other_member = chat.member.exclude(user=request.user).first()
        return other_member.user.id


class MessageMetadataSerializer(ModelSerializer):
    class Meta:
        model = MessageMetadataModel
        fields = (
            "message",
            "file_url",
            "file_size",
            "file_name",
        )


class MessageEditSerializer(ModelSerializer):
    class Meta:
        model = MessageEditModel
        fields = (
            "message",
            "old_message",
            "new_message",
            "edited_by",
        )


class MessageForwardSerializer(ModelSerializer):
    class Meta:
        model = MessageForwardModel
        fields = (
            "message",
            "original_sender",
            "original_chat",
            "forward_by",
            "forward_at",
        )


class MessageHashtagSerializer(ModelSerializer):
    class Meta:
        model = MessageHashtagModel
        fields = (
            "message",
            "hashtag",
            "normalized_hashtag",
            "position_start",
            "position_end",
        )


class MessageLinkSerializer(ModelSerializer):
    class Meta:
        model = MessageLinkModel
        fields = (
            "message",
            "url",
            "text",
            "image_url",
            "domain",
        )


class MessageReactionSerializer(ModelSerializer):
    class Meta:
        model = MessageReactionModel
        fields = (
            "chat",
            "user",
            "message",
            "create_at",
            "update_at",
        )


class MessageReplaysSerializer(ModelSerializer):
    class Meta:
        model = MessageReplaysModel
        fields = (
            "message",
            "reply_to",
            "text",
            "created_at",
        )


class CreateMessageSerializer(Serializer):
    chat = serializers.PrimaryKeyRelatedField(
        queryset=ChatModel.objects.all(), required=True
    )
    message_type = serializers.PrimaryKeyRelatedField(
        queryset=MessagesTypeModel.objects.all()
    )
    message = serializers.CharField()

    def create(self, validated_data):
        sender = self.context["sender"]

        print(validated_data)

        message = MessagesModel.objects.create(**validated_data, sender=sender)

        return message
