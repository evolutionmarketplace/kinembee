"""
Admin configuration for categories app.
"""
from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Category, CategoryAttribute, CategoryTag, CategoryTagAssignment


@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    """
    Admin interface for Category model.
    """
    list_display = [
        'name', 'category_type', 'is_active', 'featured',
        'product_count', 'sort_order', 'level'
    ]
    list_filter = ['category_type', 'is_active', 'featured', 'show_in_menu']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['tree_id', 'lft']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'parent')
        }),
        ('Display', {
            'fields': ('icon', 'image', 'category_type', 'sort_order')
        }),
        ('Settings', {
            'fields': ('is_active', 'featured', 'show_in_menu')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
    )

    actions = ['activate_categories', 'deactivate_categories', 'feature_categories']

    def activate_categories(self, request, queryset):
        count = queryset.update(is_active=True)
        self.message_user(request, f'{count} categories have been activated.')
    activate_categories.short_description = 'Activate selected categories'

    def deactivate_categories(self, request, queryset):
        count = queryset.update(is_active=False)
        self.message_user(request, f'{count} categories have been deactivated.')
    deactivate_categories.short_description = 'Deactivate selected categories'

    def feature_categories(self, request, queryset):
        count = queryset.update(featured=True)
        self.message_user(request, f'{count} categories have been featured.')
    feature_categories.short_description = 'Feature selected categories'


@admin.register(CategoryAttribute)
class CategoryAttributeAdmin(admin.ModelAdmin):
    """
    Admin interface for CategoryAttribute model.
    """
    list_display = [
        'name', 'category', 'attribute_type', 'is_required',
        'is_filterable', 'sort_order'
    ]
    list_filter = ['attribute_type', 'is_required', 'is_filterable']
    search_fields = ['name', 'category__name']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['category', 'sort_order', 'name']


@admin.register(CategoryTag)
class CategoryTagAdmin(admin.ModelAdmin):
    """
    Admin interface for CategoryTag model.
    """
    list_display = ['name', 'slug', 'color']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(CategoryTagAssignment)
class CategoryTagAssignmentAdmin(admin.ModelAdmin):
    """
    Admin interface for CategoryTagAssignment model.
    """
    list_display = ['category', 'tag']
    list_filter = ['tag']
    search_fields = ['category__name', 'tag__name']