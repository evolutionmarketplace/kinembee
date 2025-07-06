"""
Product models for Evolution Digital Market.
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from taggit.managers import TaggableManager
from apps.core.models import SoftDeleteModel, Address, SEOModel
from apps.categories.models import Category
import uuid

User = get_user_model()


class Product(SoftDeleteModel, SEOModel):
    """
    Main product model for marketplace listings.
    """
    CONDITION_CHOICES = [
        ('new', 'New'),
        ('used', 'Used'),
        ('refurbished', 'Refurbished'),
    ]

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('sold', 'Sold'),
        ('expired', 'Expired'),
        ('suspended', 'Suspended'),
    ]

    # Basic information
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    
    # Categorization
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    subcategory = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='subcategory_products'
    )
    
    # Product details
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    brand = models.CharField(max_length=100, blank=True)
    model = models.CharField(max_length=100, blank=True)
    
    # Seller information
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    
    # Location
    location = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    pickup_available = models.BooleanField(default=True)
    delivery_available = models.BooleanField(default=False)
    shipping_cost = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    
    # Status and visibility
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_boosted = models.BooleanField(default=False)
    boost_expires_at = models.DateTimeField(null=True, blank=True)
    
    # Engagement metrics
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    shares = models.PositiveIntegerField(default=0)
    
    # Timing
    expires_at = models.DateTimeField(null=True, blank=True)
    sold_at = models.DateTimeField(null=True, blank=True)
    
    # Additional data
    attributes = models.JSONField(default=dict, blank=True)
    tags = TaggableManager(blank=True)
    
    class Meta:
        db_table = 'products'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'is_active']),
            models.Index(fields=['category', 'price']),
            models.Index(fields=['seller', 'status']),
            models.Index(fields=['is_boosted', 'boost_expires_at']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def is_expired(self):
        return self.expires_at and timezone.now() > self.expires_at

    @property
    def is_boost_active(self):
        return self.is_boosted and (not self.boost_expires_at or timezone.now() < self.boost_expires_at)

    @property
    def main_image(self):
        return self.images.filter(is_primary=True).first() or self.images.first()

    def mark_as_sold(self, buyer=None):
        """Mark product as sold."""
        self.status = 'sold'
        self.sold_at = timezone.now()
        self.is_active = False
        self.save()
        
        if buyer:
            ProductSale.objects.create(
                product=self,
                seller=self.seller,
                buyer=buyer,
                sale_price=self.price
            )

    def boost_listing(self, duration_days=7):
        """Boost the listing for better visibility."""
        self.is_boosted = True
        self.boost_expires_at = timezone.now() + timezone.timedelta(days=duration_days)
        self.save()

    def increment_views(self):
        """Increment view count."""
        self.views += 1
        self.save(update_fields=['views'])


class ProductImage(models.Model):
    """
    Product images with ordering and primary image designation.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    thumbnail = models.ImageField(upload_to='products/thumbnails/', blank=True)
    alt_text = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'product_images'
        ordering = ['sort_order', 'created_at']

    def __str__(self):
        return f"Image for {self.product.title}"

    def save(self, *args, **kwargs):
        # Ensure only one primary image per product
        if self.is_primary:
            ProductImage.objects.filter(
                product=self.product,
                is_primary=True
            ).exclude(id=self.id).update(is_primary=False)
        super().save(*args, **kwargs)


class ProductWishlist(models.Model):
    """
    User wishlist/favorites for products.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlisted_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'product_wishlist'
        unique_together = ['user', 'product']

    def __str__(self):
        return f"{self.user.email} - {self.product.title}"


class ProductView(models.Model):
    """
    Track product views for analytics.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='view_records')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'product_views'
        indexes = [
            models.Index(fields=['product', 'created_at']),
            models.Index(fields=['user', 'created_at']),
        ]

    def __str__(self):
        return f"View of {self.product.title}"


class ProductSale(models.Model):
    """
    Record of product sales.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sales')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sales_made')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases_made')
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    commission = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'product_sales'

    def __str__(self):
        return f"Sale of {self.product.title} to {self.buyer.email}"


class ProductReport(models.Model):
    """
    User reports for inappropriate products.
    """
    REPORT_REASONS = [
        ('spam', 'Spam'),
        ('inappropriate', 'Inappropriate Content'),
        ('fake', 'Fake/Counterfeit'),
        ('overpriced', 'Overpriced'),
        ('duplicate', 'Duplicate Listing'),
        ('prohibited', 'Prohibited Item'),
        ('other', 'Other'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reports')
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_reports')
    reason = models.CharField(max_length=20, choices=REPORT_REASONS)
    description = models.TextField(blank=True)
    is_resolved = models.BooleanField(default=False)
    resolved_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='resolved_reports'
    )
    resolved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'product_reports'
        unique_together = ['product', 'reporter']

    def __str__(self):
        return f"Report for {self.product.title} by {self.reporter.email}"


class SavedSearch(models.Model):
    """
    User saved searches with alerts.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_searches')
    name = models.CharField(max_length=100)
    query = models.CharField(max_length=200, blank=True)
    filters = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)
    email_alerts = models.BooleanField(default=True)
    last_alert_sent = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'saved_searches'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.name}"