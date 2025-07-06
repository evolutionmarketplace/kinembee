"""
Serializers for notifications.
"""
from rest_framework import serializers
from .models import Notification, NotificationPreference, NotificationDevice


class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer for notifications.
    """
    sender_name = serializers.CharField(source='sender.full_name', read_only=True)
    time_ago = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = [
            'id', 'title', 'message', 'priority', 'is_read', 'read_at',
            'sender_name', 'action_url', 'data', 'created_at', 'time_ago'
        ]

    def get_time_ago(self, obj):
        from django.utils import timezone
        from datetime import timedelta
        
        now = timezone.now()
        diff = now - obj.created_at
        
        if diff < timedelta(minutes=1):
            return "Just now"
        elif diff < timedelta(hours=1):
            return f"{diff.seconds // 60}m ago"
        elif diff < timedelta(days=1):
            return f"{diff.seconds // 3600}h ago"
        elif diff < timedelta(days=7):
            return f"{diff.days}d ago"
        else:
            return obj.created_at.strftime("%b %d")


class NotificationPreferenceSerializer(serializers.ModelSerializer):
    """
    Serializer for notification preferences.
    """
    class Meta:
        model = NotificationPreference
        exclude = ['id', 'user', 'created_at', 'updated_at']


class NotificationDeviceSerializer(serializers.ModelSerializer):
    """
    Serializer for notification devices.
    """
    class Meta:
        model = NotificationDevice
        fields = ['id', 'device_type', 'device_token', 'device_name', 'is_active']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return NotificationDevice.objects.create(**validated_data)