from django.db import models
from apps.chats.models import ChatModel
from apps.user.models import UserModel

# Create your models here.


class MessagesTypeModel(models.Model):
    class Meta:
        db_table = "messages_type"

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    code = models.CharField(max_length=100)


class MessagesModel(models.Model):
    class Meta:
        db_table = "messages"

    chat = models.ForeignKey(
        ChatModel, on_delete=models.CASCADE, related_name="chat_messages"
    )
    sender = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name="sent_messages"
    )
    message_type = models.ForeignKey(
        MessagesTypeModel, on_delete=models.CASCADE, related_name="messages"
    )
    message = models.CharField(max_length=250)
    is_edited = models.BooleanField(default=False)
    is_delited = models.BooleanField(default=False)
    is_pined = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


class MessageMetadataModel(models.Model):
    class Meta:
        db_table = "message_metadata"

    message = models.ForeignKey(
        MessagesModel, on_delete=models.CASCADE, related_name="metadata"
    )
    file_url = models.CharField(max_length=250)
    file_size = models.IntegerField()
    file_name = models.CharField(max_length=100)


class MessageForwardModel(models.Model):
    class Meta:
        db_table = "message_forward"

    message = models.ForeignKey(
        MessagesModel, on_delete=models.CASCADE, related_name="forwards"
    )

    original_sender = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name="sent_forwards"
    )

    original_chat = models.ForeignKey(
        ChatModel, on_delete=models.CASCADE, related_name="chat_forwards"
    )

    forward_by = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name="user_forwards"
    )

    forward_at = models.DateTimeField(auto_now_add=True)


class MessageEditModel(models.Model):
    class Meta:
        db_table = "messages_edit"

    message = models.ForeignKey(
        MessagesModel, on_delete=models.CASCADE, related_name="edits"
    )

    old_message = models.TextField()
    new_message = models.TextField()

    edited_by = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name="edited_messages"
    )

    created_at = models.DateTimeField(auto_now_add=True)


class MessageReactionModel(models.Model):
    class Meta:
        db_table = "message_reaction"

    chat = models.ForeignKey(
        ChatModel, on_delete=models.CASCADE, related_name="chat_reactions"
    )
    user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name="user_reactions"
    )
    message = models.ForeignKey(
        MessagesModel, on_delete=models.CASCADE, related_name="reactions"
    )
    type = models.CharField(max_length=50)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


class MessageStatusModel(models.Model):
    class Meta:
        db_table = "message_status"

    message = models.ForeignKey(
        MessagesModel, on_delete=models.CASCADE, related_name="statuses"
    )
    user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name="message_statuses"
    )
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)


class MessageLinkModel(models.Model):
    class Meta:
        db_table = "message_link"

    message = models.ForeignKey(
        MessagesModel, on_delete=models.CASCADE, related_name="links"
    )
    url = models.URLField()
    text = models.TextField(null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)
    domain = models.CharField(max_length=255)


class MessageHashtagModel(models.Model):
    class Meta:
        db_table = "message_hashtag"

    message = models.ForeignKey(
        MessagesModel, on_delete=models.CASCADE, related_name="hashtags"
    )
    hashtag = models.CharField(max_length=100)
    normalized_hashtag = models.CharField(max_length=100)
    position_start = models.IntegerField()
    position_end = models.IntegerField()


class MessageReplaysModel(models.Model):
    class Meta:
        db_table = "message_replays"

    mmessage = models.ForeignKey(
        MessagesModel, on_delete=models.CASCADE, related_name="replies_sent"
    )
    reply_to = models.ForeignKey(
        MessagesModel, on_delete=models.CASCADE, related_name="replies_received"
    )
    text = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
