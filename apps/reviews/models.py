"""
Review models for Evolution Digital Market.
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.core.models import TimeStampedModel
from apps.products.models import Product
import uuid

User = get_user_model()


class Review(TimeStampedModel):
    """
    Product and seller reviews.
    """
    REVIEW_TYPES = [
        ('product', 'Product Review'),
        ('seller', 'Seller Review'),
        ('buyer', 'Buyer Review'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_given')
    reviewee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_received')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    
    review_type = models.CharField(max_length=10, choices=REVIEW_TYPES, default='product')
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    title = models.CharField(max_length=200, blank=True)
    comment = models.TextField()
    
    # Detailed ratings
    communication_rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True, blank=True
    )
    delivery_rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True, blank=True
    )
    item_description_rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True, blank=True
    )
    
    # Status
    is_verified = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_flagged = models.BooleanField(default=False)
    
    # Engagement
    helpful_count = models.PositiveIntegerField(default=0)
    
    class Meta:
        db_table = 'reviews'
        unique_together = ['reviewer', 'product', 'review_type']
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['reviewee', 'rating']),
            models.Index(fields=['product', 'rating']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"Review by {self.reviewer.email} for {self.product.title}"

    @property
    def average_detailed_rating(self):
        """Calculate average of detailed ratings."""
        ratings = [
            self.communication_rating,
            self.delivery_rating,
            self.item_description_rating
        ]
        valid_ratings = [r for r in ratings if r is not None]
        return sum(valid_ratings) / len(valid_ratings) if valid_ratings else self.rating


class ReviewImage(TimeStampedModel):
    """
    Images attached to reviews.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='reviews/')
    caption = models.CharField(max_length=200, blank=True)

    class Meta:
        db_table = 'review_images'

    def __str__(self):
        return f"Image for review {self.review.id}"


class ReviewHelpful(TimeStampedModel):
    """
    Track users who found reviews helpful.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='helpful_votes')

    class Meta:
        db_table = 'review_helpful'
        unique_together = ['user', 'review']

    def __str__(self):
        return f"{self.user.email} found review {self.review.id} helpful"


class ReviewResponse(TimeStampedModel):
    """
    Seller responses to reviews.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    review = models.OneToOneField(Review, on_delete=models.CASCADE, related_name='response')
    responder = models.ForeignKey(User, on_delete=models.CASCADE)
    response = models.TextField()

    class Meta:
        db_table = 'review_responses'

    def __str__(self):
        return f"Response to review {self.review.id}"


class ReviewReport(TimeStampedModel):
    """
    Reports for inappropriate reviews.
    """
    REPORT_REASONS = [
        ('spam', 'Spam'),
        ('inappropriate', 'Inappropriate Content'),
        ('fake', 'Fake Review'),
        ('offensive', 'Offensive Language'),
        ('irrelevant', 'Irrelevant'),
        ('other', 'Other'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='reports')
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.CharField(max_length=20, choices=REPORT_REASONS)
    description = models.TextField(blank=True)
    is_resolved = models.BooleanField(default=False)
    resolved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='resolved_review_reports'
    )
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'review_reports'
        unique_together = ['review', 'reporter']

    def __str__(self):
        return f"Report for review {self.review.id} by {self.reporter.email}"