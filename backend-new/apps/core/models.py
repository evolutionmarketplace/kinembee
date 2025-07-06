"""
Core models for Evolution Digital Market.
"""
from django.db import models
from django.utils import timezone
import uuid


class TimeStampedModel(models.Model):
    """
    Abstract base class that provides self-updating 'created_at' and 'updated_at' fields.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteManager(models.Manager):
    """
    Manager that excludes soft-deleted objects by default.
    """
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class SoftDeleteModel(TimeStampedModel):
    """
    Abstract base class that provides soft delete functionality.
    """
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        """
        Soft delete the object.
        """
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(using=using)

    def hard_delete(self, using=None, keep_parents=False):
        """
        Permanently delete the object.
        """
        super().delete(using=using, keep_parents=keep_parents)

    def restore(self):
        """
        Restore a soft-deleted object.
        """
        self.is_deleted = False
        self.deleted_at = None
        self.save()


class Address(TimeStampedModel):
    """
    Address model for users and listings.
    """
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='United States')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return f"{self.street_address}, {self.city}, {self.state} {self.postal_code}"

    @property
    def full_address(self):
        return f"{self.street_address}, {self.city}, {self.state} {self.postal_code}, {self.country}"


class SEOModel(models.Model):
    """
    Abstract model for SEO fields.
    """
    meta_title = models.CharField(max_length=60, blank=True, help_text="SEO title (max 60 characters)")
    meta_description = models.CharField(max_length=160, blank=True, help_text="SEO description (max 160 characters)")
    meta_keywords = models.CharField(max_length=255, blank=True, help_text="SEO keywords, comma separated")
    
    class Meta:
        abstract = True