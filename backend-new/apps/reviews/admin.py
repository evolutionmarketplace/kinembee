"""
Admin configuration for reviews app.
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import Review, ReviewImage, ReviewHelpful, ReviewResponse, ReviewReport


class ReviewImageInline(admin.TabularInline):
    """
    Inline admin for review images.
    """
    model = ReviewImage
    extra = 0
    fields = ['image', 'caption']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Admin interface for Review model.
    """
    list_display = [
        'reviewer', 'reviewee', 'product', 'rating', 'review_type',
        'is_verified', 'is_featured', 'helpful_count', 'created_at'
    ]
    list_filter = [
        'review_type', 'rating', 'is_verified', 'is_featured',
        'is_flagged', 'created_at'
    ]
    search_fields = [
        'reviewer__email', 'reviewee__email', 'product__title',
        'title', 'comment'
    ]
    readonly_fields = ['helpful_count', 'created_at', 'updated_at']
    inlines = [ReviewImageInline]
    
    fieldsets = (
        ('Review Information', {
            'fields': ('reviewer', 'reviewee', 'product', 'review_type')
        }),
        ('Rating & Content', {
            'fields': ('rating', 'title', 'comment')
        }),
        ('Detailed Ratings', {
            'fields': ('communication_rating', 'delivery_rating', 'item_description_rating')
        }),
        ('Status', {
            'fields': ('is_verified', 'is_featured', 'is_flagged')
        }),
        ('Engagement', {
            'fields': ('helpful_count',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['verify_reviews', 'feature_reviews', 'flag_reviews']

    def verify_reviews(self, request, queryset):
        count = queryset.update(is_verified=True)
        self.message_user(request, f'{count} reviews have been verified.')
    verify_reviews.short_description = 'Verify selected reviews'

    def feature_reviews(self, request, queryset):
        count = queryset.update(is_featured=True)
        self.message_user(request, f'{count} reviews have been featured.')
    feature_reviews.short_description = 'Feature selected reviews'

    def flag_reviews(self, request, queryset):
        count = queryset.update(is_flagged=True)
        self.message_user(request, f'{count} reviews have been flagged.')
    flag_reviews.short_description = 'Flag selected reviews'


@admin.register(ReviewResponse)
class ReviewResponseAdmin(admin.ModelAdmin):
    """
    Admin interface for ReviewResponse model.
    """
    list_display = ['review', 'responder', 'created_at']
    search_fields = ['review__title', 'responder__email', 'response']
    readonly_fields = ['created_at']


@admin.register(ReviewReport)
class ReviewReportAdmin(admin.ModelAdmin):
    """
    Admin interface for ReviewReport model.
    """
    list_display = ['review', 'reporter', 'reason', 'is_resolved', 'created_at']
    list_filter = ['reason', 'is_resolved', 'created_at']
    search_fields = ['review__title', 'reporter__email', 'description']
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