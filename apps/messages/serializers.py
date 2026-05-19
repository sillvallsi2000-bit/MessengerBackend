from django.utils import timezone
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer

from apps.chats.models import ChatModel
from core.services.chat_service import getUsersFromChat, notifyMessage

from .models import (
    MessageEditModel,
    MessageForwardModel,
    MessageHashtagModel,
    MessageLinkModel,
    MessageMetadataModel,
    MessageReactionModel,
    MessagesModel,
    MessageStatusModel,
    MessagesTypeModel,
)


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


class MessageMetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageMetadataModel
        fields = ["file_url", "file_size", "file_name"]


class MessagesSerializer(ModelSerializer):
    target_id = serializers.SerializerMethodField()
    metadata = MessageMetadataSerializer(many=True, read_only=True)
    reply_to = serializers.SerializerMethodField()

    class Meta:
        model = MessagesModel
        fields = (
            "id",
            "chat",
            "metadata",
            "sender",
            "message_type",
            "message",
            "is_edited",
            "is_delited",
            "is_pined",
            "create_at",
            "update_at",
            "target_id",
            "reply_to",
        )

    def get_target_id(self, obj):
        request = self.context.get("request")
        if not request:
            return None
        chat = obj.chat
        other_member = chat.member.exclude(user=request.user).first()
        return other_member.user.id

    def get_reply_to(self, obj):
        if obj.reply_to is None:
            return None
        return {
            "id": obj.reply_to.id,
            "sender": obj.reply_to.sender.username,
            "message": obj.reply_to.message,
        }


class MessageRetrieveUpdateDestroySerializer(ModelSerializer):
    class Meta:
        model = MessagesModel
        fields = ["id", "message", "is_edited", "is_delited", "is_pined"]
        read_only_fields = ["id", "is_edited", "is_delited"]

    def update(self, instance, validated_data):
        validated_data["is_edited"] = True
        return super().update(instance, validated_data)


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
            "forwarded_message",
            "original_message",
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
            "message",
            "create_at",
            "type",
            "update_at",
        )

    def create(self, validated_data):
        user = self.context["user"]
        reaction, created = MessageReactionModel.objects.update_or_create(
            user=user,
            message=validated_data["message"],
            defaults={"type": validated_data["type"]},
        )
        return reaction


class CreateMessageSerializer(Serializer):
    reply_to = serializers.PrimaryKeyRelatedField(
        queryset=MessagesModel.objects.all(), required=False, allow_null=True
    )
    chat = serializers.PrimaryKeyRelatedField(
        queryset=ChatModel.objects.all(), required=True
    )
    message_type = serializers.PrimaryKeyRelatedField(
        queryset=MessagesTypeModel.objects.all(), required=False
    )
    message = serializers.CharField(required=False, allow_blank=True, default="")

    def validate(self, attrs):
        if not attrs.get("message_type"):
            attrs["message_type"] = MessagesTypeModel.objects.get(id=1)
        return attrs

    def create(self, validated_data):
        sender = self.context["sender"]
        chat = validated_data.get("chat")
        message = MessagesModel.objects.create(**validated_data, sender=sender)
        chat.last_message = message
        chat.last_activity = timezone.now()
        chat.save()
        getUsersFromChat(chat)
        return message


class CreateForwardMessageSerializer(Serializer):
    original_message = serializers.PrimaryKeyRelatedField(
        queryset=MessagesModel.objects.all(), write_only=True
    )

    target_chat = serializers.PrimaryKeyRelatedField(
        queryset=ChatModel.objects.all(), write_only=True
    )

    def create(self, validated_data):
        request = self.context["request"]
        original_message = self.validated_data["original_message"]
        target_chat = self.validated_data["target_chat"]

        forward_message = MessagesModel.objects.create(
            chat=target_chat,
            sender=request.user,
            message=original_message.message,
            message_type=original_message.message_type,
        )

        MessageForwardModel.objects.create(
            forwarded_message=forward_message,
            original_message=original_message,
            forward_by=request.user,
        )

        target_chat.last_message = forward_message
        target_chat.last_activity = timezone.now()
        target_chat.save()
        getUsersFromChat(chat=target_chat)
        notifyMessage(target_chat.id, forward_message, user=request.user)
        return forward_message
