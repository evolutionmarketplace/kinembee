"""
Category models for Evolution Digital Market.
"""
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from apps.core.models import TimeStampedModel, SEOModel
from django.utils.text import slugify


class Category(MPTTModel, TimeStampedModel, SEOModel):
    """
    Hierarchical category model using MPTT.
    """
    CATEGORY_TYPES = [
        ('goods', 'Goods'),
        ('services', 'Services'),
        ('both', 'Both'),
    ]

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Lucide icon name")
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    
    category_type = models.CharField(max_length=10, choices=CATEGORY_TYPES, default='goods')
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    
    # SEO and display
    featured = models.BooleanField(default=False)
    show_in_menu = models.BooleanField(default=True)
    
    # Statistics
    product_count = models.PositiveIntegerField(default=0)
    
    class MPTTMeta:
        order_insertion_by = ['sort_order', 'name']

    class Meta:
        db_table = 'categories'
        verbose_name_plural = 'Categories'
        ordering = ['sort_order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def full_path(self):
        """Get full category path."""
        ancestors = self.get_ancestors(include_self=True)
        return ' > '.join([cat.name for cat in ancestors])

    def get_absolute_url(self):
        return f"/categories/{self.slug}/"

    def update_product_count(self):
        """Update product count for this category."""
        from apps.products.models import Product
        self.product_count = Product.objects.filter(
            category=self,
            is_active=True
        ).count()
        self.save(update_fields=['product_count'])


class CategoryAttribute(TimeStampedModel):
    """
    Attributes that can be associated with categories.
    """
    ATTRIBUTE_TYPES = [
        ('text', 'Text'),
        ('number', 'Number'),
        ('boolean', 'Boolean'),
        ('choice', 'Choice'),
        ('multi_choice', 'Multiple Choice'),
        ('date', 'Date'),
        ('url', 'URL'),
    ]

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='attributes')
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120)
    attribute_type = models.CharField(max_length=20, choices=ATTRIBUTE_TYPES)
    is_required = models.BooleanField(default=False)
    is_filterable = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    
    # For choice types
    choices = models.JSONField(default=list, blank=True, help_text="List of choices for choice/multi_choice types")
    
    # Validation
    min_value = models.FloatField(null=True, blank=True, help_text="Minimum value for number type")
    max_value = models.FloatField(null=True, blank=True, help_text="Maximum value for number type")
    min_length = models.PositiveIntegerField(null=True, blank=True, help_text="Minimum length for text type")
    max_length = models.PositiveIntegerField(null=True, blank=True, help_text="Maximum length for text type")

    class Meta:
        db_table = 'category_attributes'
        unique_together = ['category', 'slug']
        ordering = ['sort_order', 'name']

    def __str__(self):
        return f"{self.category.name} - {self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class CategoryTag(TimeStampedModel):
    """
    Tags for categories to improve search and organization.
    """
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True, blank=True)
    color = models.CharField(max_length=7, default='#3B82F6', help_text="Hex color code")
    
    class Meta:
        db_table = 'category_tags'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class CategoryTagAssignment(TimeStampedModel):
    """
    Many-to-many relationship between categories and tags.
    """
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='tag_assignments')
    tag = models.ForeignKey(CategoryTag, on_delete=models.CASCADE, related_name='category_assignments')

    class Meta:
        db_table = 'category_tag_assignments'
        unique_together = ['category', 'tag']

    def __str__(self):
        return f"{self.category.name} - {self.tag.name}"