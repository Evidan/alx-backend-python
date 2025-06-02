from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'user_id',
            'username',
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'full_name'
        ]

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class MessageSerializer(serializers.ModelSerializer):
    message_body = serializers.CharField()
    sender_name = serializers.SerializerMethodField()
    sender_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = Message
        fields = [
            'message_id',
            'conversation',
            'sender_id',
            'sender_name',
            'message_body',
            'sent_at'
        ]
        read_only_fields = ['message_id', 'sent_at', 'sender_name']

    def get_sender_name(self, obj):
        return f"{obj.sender.first_name} {obj.sender.last_name}"

    def validate_message_body(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message body cannot be empty.")
        return value

    def create(self, validated_data):
        sender_id = validated_data.pop('sender_id')
        validated_data['sender'] = User.objects.get(user_id=sender_id)
        return super().create(validated_data)


class ConversationSerializer(serializers.ModelSerializer):
    participant_ids = serializers.ListField(
        child=serializers.UUIDField(), write_only=True
    )
    participants = UserSerializer(many=True, read_only=True)
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participant_ids',
            'participants',
            'created_at',
            'messages'
        ]
        read_only_fields = ['conversation_id', 'created_at', 'participants', 'messages']

    def get_messages(self, obj):
        messages = obj.messages.order_by('sent_at')
        return MessageSerializer(messages, many=True).data

    def create(self, validated_data):
        participant_ids = validated_data.pop('participant_ids', [])
        if not participant_ids or len(participant_ids) < 2:
            raise serializers.ValidationError("A conversation must include at least 2 participants.")

        conversation = Conversation.objects.create(**validated_data)
        users = User.objects.filter(user_id__in=participant_ids)
        conversation.participants.set(users)
        return conversation
