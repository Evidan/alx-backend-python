from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all().prefetch_related('participants', 'messages')
    serializer_class = ConversationSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__username']

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return self.queryset.filter(participants=user)
        return self.queryset.none()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().select_related('conversation', 'sender')
    serializer_class = MessageSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.OrderingFilter]
    ordering = ['sent_at']

    def get_queryset(self):
        conversation_id = self.request.query_params.get('conversation_id')
        if conversation_id:
            return self.queryset.filter(conversation__conversation_id=conversation_id)
        return self.queryset.none()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
