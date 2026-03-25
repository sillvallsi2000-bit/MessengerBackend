from django.shortcuts import render
from .serializers import (
    ModelSerializer,
    MessageForwardSerializer,
    MessageEditSerializer,
    MessageHashtagSerializer,
    MessageLinkSerializer,
    MessageMetadataSerializer,
    MessageReactionSerializer,
    MessageReplaysSerializer,
    MessagesSerializer,
    MessageStatusSerializer,
    MessagesTypeSerializer,
)
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
