"""
Notification models for Evolution Digital Market.
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from apps.core.models import TimeStampedModel
import uuid

User = get_user_model()


class NotificationTemplate(TimeStampedModel):
    """
    Templates for different types of notifications.
    """
    NOTIFICATION_TYPES = [
        ('new_message', 'New Message'),
        ('product_sold', 'Product Sold'),
        ('product_liked', 'Product Liked'),
        ('review_received', 'Review Received'),
        ('price_drop', 'Price Drop Alert'),
        ('new_listing', 'New Listing in Category'),
        ('payment_received', 'Payment Received'),
        ('account_verified', 'Account Verified'),
        ('listing_expired', 'Listing Expired'),
        ('boost_expired', 'Boost Expired'),
        ('system_announcement', 'System Announcement'),
    ]

    name = models.CharField(max_length=100, unique=True)
    notification_type = models.CharField(max_length=30, choices=NOTIFICATION_TYPES)
    title_template = models.CharField(max_length=200)
    message_template = models.TextField()
    email_template = models.TextField(blank=True)
    sms_template = models.CharField(max_length=160, blank=True)
    is_active = models.BooleanField(default=True)
    
    # Delivery settings
    send_push = models.BooleanField(default=True)
    send_email = models.BooleanField(default=False)
    send_sms = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'notification_templates'

    def __str__(self):
        return self.name


class Notification(TimeStampedModel):
    """
    Individual notifications sent to users.
    """
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='sent_notifications'
    )
    
    template = models.ForeignKey(
        NotificationTemplate, 
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    
    title = models.CharField(max_length=200)
    message = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='normal')
    
    # Generic relation to any model
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.CharField(max_length=50, null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # Status tracking
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    
    # Delivery tracking
    push_sent = models.BooleanField(default=False)
    push_sent_at = models.DateTimeField(null=True, blank=True)
    email_sent = models.BooleanField(default=False)
    email_sent_at = models.DateTimeField(null=True, blank=True)
    sms_sent = models.BooleanField(default=False)
    sms_sent_at = models.DateTimeField(null=True, blank=True)
    
    # Additional data
    data = models.JSONField(default=dict, blank=True)
    action_url = models.URLField(blank=True)
    
    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'is_read']),
            models.Index(fields=['created_at']),
            models.Index(fields=['priority']),
        ]

    def __str__(self):
        return f"Notification to {self.recipient.email}: {self.title}"

    def mark_as_read(self):
        """Mark notification as read."""
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=['is_read', 'read_at'])


class NotificationPreference(TimeStampedModel):
    """
    User preferences for different types of notifications.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_preferences')
    
    # Push notification preferences
    push_new_messages = models.BooleanField(default=True)
    push_product_updates = models.BooleanField(default=True)
    push_price_alerts = models.BooleanField(default=True)
    push_reviews = models.BooleanField(default=True)
    push_marketing = models.BooleanField(default=False)
    
    # Email notification preferences
    email_new_messages = models.BooleanField(default=True)
    email_product_updates = models.BooleanField(default=True)
    email_price_alerts = models.BooleanField(default=True)
    email_reviews = models.BooleanField(default=True)
    email_marketing = models.BooleanField(default=True)
    email_weekly_digest = models.BooleanField(default=True)
    
    # SMS notification preferences
    sms_urgent_only = models.BooleanField(default=True)
    sms_security_alerts = models.BooleanField(default=True)
    sms_payment_confirmations = models.BooleanField(default=True)
    
    # Quiet hours
    quiet_hours_enabled = models.BooleanField(default=False)
    quiet_hours_start = models.TimeField(null=True, blank=True)
    quiet_hours_end = models.TimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'notification_preferences'

    def __str__(self):
        return f"Notification preferences for {self.user.email}"


class NotificationDevice(TimeStampedModel):
    """
    User devices for push notifications.
    """
    DEVICE_TYPES = [
        ('ios', 'iOS'),
        ('android', 'Android'),
        ('web', 'Web Browser'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notification_devices')
    device_type = models.CharField(max_length=10, choices=DEVICE_TYPES)
    device_token = models.TextField()
    device_name = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    last_used = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'notification_devices'
        unique_together = ['user', 'device_token']

    def __str__(self):
        return f"{self.user.email} - {self.device_type}"


class NotificationBatch(TimeStampedModel):
    """
    Batch notifications for bulk sending.
    """
    name = models.CharField(max_length=100)
    template = models.ForeignKey(NotificationTemplate, on_delete=models.CASCADE)
    recipients = models.ManyToManyField(User, related_name='notification_batches')
    
    # Scheduling
    scheduled_at = models.DateTimeField(null=True, blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    
    # Status
    is_sent = models.BooleanField(default=False)
    total_recipients = models.PositiveIntegerField(default=0)
    successful_sends = models.PositiveIntegerField(default=0)
    failed_sends = models.PositiveIntegerField(default=0)
    
    class Meta:
        db_table = 'notification_batches'

    def __str__(self):
        return self.name