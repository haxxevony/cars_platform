from rest_framework import serializers
from .models import Notification
from django.conf import settings

class NotificationSerializer(serializers.ModelSerializer):
    recipient = serializers.StringRelatedField(read_only=True)
    timestamp = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'message', 'is_read', 'notification_type', 'timestamp']
        read_only_fields = ['id', 'recipient', 'timestamp']

    def validate_message(self, value):
        if not value.strip():
            raise serializers.ValidationError('Message cannot be empty.')
        if len(value) > 500:
            raise serializers.ValidationError('Message cannot exceed 500 characters.')
        return value

    def validate_notification_type(self, value):
        valid_types = [choice[0] for choice in Notification._meta.get_field('notification_type').choices]
        if value not in valid_types:
            raise serializers.ValidationError('Invalid notification type.')
        return value

    def create(self, validated_data):
        validated_data['recipient'] = self.context['request'].user
        return super().create(validated_data)