# chats/permissions.py
from rest_framework import permissions
from .models import Conversation

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to access it.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        conversation = getattr(obj, 'conversation', None)
        if not conversation:
            return False
        return request.user in conversation.participants.all()
