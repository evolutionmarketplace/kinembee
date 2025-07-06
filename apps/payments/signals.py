"""
Signals for payments app.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Wallet
from apps.accounts.models import User


@receiver(post_save, sender=User)
def create_user_wallet(sender, instance, created, **kwargs):
    """
    Create wallet when user is created.
    """
    if created:
        Wallet.objects.get_or_create(user=instance)