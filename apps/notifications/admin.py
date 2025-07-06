"""
Admin configuration for notifications app.
"""
from django.contrib import admin
from .models import (
    NotificationTemplate, Notification, NotificationPreference,
    NotificationDevice, NotificationBatch
)


@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):
    """
    Admin interface for NotificationTemplate model.
    """
    list_display = [
        'name', 'notification_type', 'is_active', 'send_push', 
        'send_email', 'send_sms', 'created_at'
    ]
    list_filter = ['notification_type', 'is_active', 'send_push', 'send_email', 'send_sms']
    search_fields = ['name', 'title_template', 'message_template']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """
    Admin interface for Notification model.
    """
    list_display = [
        'recipient', 'title', 'priority', 'is_read', 'push_sent',
        'email_sent', 'sms_sent', 'created_at'
    ]
    list_filter = [
        'priority', 'is_read', 'push_sent', 'email_sent', 'sms_sent',
        'template__notification_type', 'created_at'
    ]
    search_fields = ['recipient__email', 'title', 'message']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    """
    Admin interface for NotificationPreference model.
    """
    list_display = [
        'user', 'push_new_messages', 'email_new_messages', 
        'sms_urgent_only', 'quiet_hours_enabled'
    ]
    search_fields = ['user__email']


@admin.register(NotificationDevice)
class NotificationDeviceAdmin(admin.ModelAdmin):
    """
    Admin interface for NotificationDevice model.
    """
    list_display = ['user', 'device_type', 'device_name', 'is_active', 'last_used']
    list_filter = ['device_type', 'is_active', 'last_used']
    search_fields = ['user__email', 'device_name']


@admin.register(NotificationBatch)
class NotificationBatchAdmin(admin.ModelAdmin):
    """
    Admin interface for NotificationBatch model.
    """
    list_display = [
        'name', 'template', 'total_recipients', 'successful_sends',
        'failed_sends', 'is_sent', 'scheduled_at'
    ]
    list_filter = ['is_sent', 'scheduled_at', 'sent_at']
    search_fields = ['name']