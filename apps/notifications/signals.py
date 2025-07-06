"""
Signals for notifications app.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import NotificationPreference
from apps.accounts.models import User


@receiver(post_save, sender=User)
def create_notification_preferences(sender, instance, created, **kwargs):
    """
    Create notification preferences when user is created.
    """
    if created:
        NotificationPreference.objects.get_or_create(user=instance)