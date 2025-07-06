"""
Signals for reviews app.
"""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg
from .models import Review


@receiver(post_save, sender=Review)
def update_user_rating(sender, instance, **kwargs):
    """
    Update user's average rating when a review is saved.
    """
    user = instance.reviewee
    profile = user.profile
    
    # Calculate new average rating
    reviews = Review.objects.filter(reviewee=user)
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    total_reviews = reviews.count()
    
    # Update profile
    profile.seller_rating = round(avg_rating, 2)
    profile.total_reviews = total_reviews
    profile.save(update_fields=['seller_rating', 'total_reviews'])


@receiver(post_delete, sender=Review)
def update_user_rating_on_delete(sender, instance, **kwargs):
    """
    Update user's average rating when a review is deleted.
    """
    user = instance.reviewee
    profile = user.profile
    
    # Calculate new average rating
    reviews = Review.objects.filter(reviewee=user)
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    total_reviews = reviews.count()
    
    # Update profile
    profile.seller_rating = round(avg_rating, 2)
    profile.total_reviews = total_reviews
    profile.save(update_fields=['seller_rating', 'total_reviews'])