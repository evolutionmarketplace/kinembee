"""
Admin configuration for products app.
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Product, ProductImage, ProductWishlist, ProductView,
    ProductSale, ProductReport, SavedSearch
)


class ProductImageInline(admin.TabularInline):
    """
    Inline admin for product images.
    """
    model = ProductImage
    extra = 1
    fields = ['image', 'alt_text', 'is_primary', 'sort_order']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin interface for Product model.
    """
    list_display = [
        'title', 'seller', 'category', 'price', 'condition',
        'status', 'is_active', 'is_boosted', 'views', 'created_at'
    ]
    list_filter = [
        'status', 'condition', 'is_active', 'is_featured', 'is_boosted',
        'category', 'created_at'
    ]
    search_fields = ['title', 'description', 'seller__email', 'brand', 'model']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['views', 'likes', 'shares', 'created_at', 'updated_at']
    inlines = [ProductImageInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description', 'price', 'condition')
        }),
        ('Categorization', {
            'fields': ('category', 'subcategory', 'brand', 'model')
        }),
        ('Seller & Location', {
            'fields': ('seller', 'location')
        }),
        ('Delivery Options', {
            'fields': ('pickup_available', 'delivery_available', 'shipping_cost')
        }),
        ('Status & Visibility', {
            'fields': ('status', 'is_active', 'is_featured', 'is_boosted', 'boost_expires_at')
        }),
        ('Engagement', {
            'fields': ('views', 'likes', 'shares'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'expires_at', 'sold_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['activate_products', 'deactivate_products', 'feature_products', 'boost_products']

    def activate_products(self, request, queryset):
        count = queryset.update(is_active=True)
        self.message_user(request, f'{count} products have been activated.')
    activate_products.short_description = 'Activate selected products'

    def deactivate_products(self, request, queryset):
        count = queryset.update(is_active=False)
        self.message_user(request, f'{count} products have been deactivated.')
    deactivate_products.short_description = 'Deactivate selected products'

    def feature_products(self, request, queryset):
        count = queryset.update(is_featured=True)
        self.message_user(request, f'{count} products have been featured.')
    feature_products.short_description = 'Feature selected products'

    def boost_products(self, request, queryset):
        from django.utils import timezone
        count = queryset.update(
            is_boosted=True,
            boost_expires_at=timezone.now() + timezone.timedelta(days=7)
        )
        self.message_user(request, f'{count} products have been boosted for 7 days.')
    boost_products.short_description = 'Boost selected products'


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    """
    Admin interface for ProductImage model.
    """
    list_display = ['product', 'is_primary', 'sort_order', 'created_at']
    list_filter = ['is_primary', 'created_at']
    search_fields = ['product__title', 'alt_text']


@admin.register(ProductWishlist)
class ProductWishlistAdmin(admin.ModelAdmin):
    """
    Admin interface for ProductWishlist model.
    """
    list_display = ['user', 'product', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__email', 'product__title']


@admin.register(ProductView)
class ProductViewAdmin(admin.ModelAdmin):
    """
    Admin interface for ProductView model.
    """
    list_display = ['product', 'user', 'ip_address', 'created_at']
    list_filter = ['created_at']
    search_fields = ['product__title', 'user__email', 'ip_address']
    readonly_fields = ['created_at']


@admin.register(ProductSale)
class ProductSaleAdmin(admin.ModelAdmin):
    """
    Admin interface for ProductSale model.
    """
    list_display = ['product', 'seller', 'buyer', 'sale_price', 'commission', 'created_at']
    list_filter = ['created_at']
    search_fields = ['product__title', 'seller__email', 'buyer__email']
    readonly_fields = ['created_at']


@admin.register(ProductReport)
class ProductReportAdmin(admin.ModelAdmin):
    """
    Admin interface for ProductReport model.
    """
    list_display = ['product', 'reporter', 'reason', 'is_resolved', 'created_at']
    list_filter = ['reason', 'is_resolved', 'created_at']
    search_fields = ['product__title', 'reporter__email', 'description']
    readonly_fields = ['created_at']

    actions = ['resolve_reports']

    def resolve_reports(self, request, queryset):
        from django.utils import timezone
        count = queryset.update(
            is_resolved=True,
            resolved_by=request.user,
            resolved_at=timezone.now()
        )
        self.message_user(request, f'{count} reports have been resolved.')
    resolve_reports.short_description = 'Resolve selected reports'


@admin.register(SavedSearch)
class SavedSearchAdmin(admin.ModelAdmin):
    """
    Admin interface for SavedSearch model.
    """
    list_display = ['user', 'name', 'is_active', 'email_alerts', 'created_at']
    list_filter = ['is_active', 'email_alerts', 'created_at']
    search_fields = ['user__email', 'name', 'query']