"""
Admin configuration for accounts app.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, UserProfile, UserPreferences, EmailVerification, PhoneVerification, UserActivity


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Admin interface for User model.
    """
    list_display = [
        'email', 'username', 'full_name', 'is_verified', 'is_business',
        'is_banned', 'date_joined', 'last_login'
    ]
    list_filter = [
        'is_verified', 'is_business', 'is_banned', 'is_staff', 'is_superuser',
        'date_joined', 'last_login'
    ]
    search_fields = ['email', 'username', 'first_name', 'last_name', 'phone_number']
    ordering = ['-date_joined']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Profile Information', {
            'fields': ('phone_number', 'avatar', 'bio', 'date_of_birth')
        }),
        ('Verification & Status', {
            'fields': ('is_verified', 'is_banned', 'ban_reason', 'banned_until')
        }),
        ('Business Information', {
            'fields': ('is_business', 'business_name', 'business_license')
        }),
        ('Preferences', {
            'fields': ('email_notifications', 'sms_notifications', 'marketing_emails')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Information', {
            'fields': ('email', 'first_name', 'last_name', 'phone_number')
        }),
    )

    def full_name(self, obj):
        return obj.full_name
    full_name.short_description = 'Full Name'

    actions = ['ban_users', 'unban_users', 'verify_users']

    def ban_users(self, request, queryset):
        count = queryset.update(is_banned=True)
        self.message_user(request, f'{count} users have been banned.')
    ban_users.short_description = 'Ban selected users'

    def unban_users(self, request, queryset):
        count = queryset.update(is_banned=False, ban_reason='', banned_until=None)
        self.message_user(request, f'{count} users have been unbanned.')
    unban_users.short_description = 'Unban selected users'

    def verify_users(self, request, queryset):
        count = queryset.update(is_verified=True)
        self.message_user(request, f'{count} users have been verified.')
    verify_users.short_description = 'Verify selected users'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Admin interface for UserProfile model.
    """
    list_display = [
        'user', 'seller_rating', 'total_sales', 'total_reviews',
        'verification_level', 'response_rate'
    ]
    list_filter = [
        'id_verified', 'address_verified', 'phone_verified',
        'email_verified', 'business_verified'
    ]
    search_fields = ['user__email', 'user__username']
    readonly_fields = ['verification_level']

    def verification_level(self, obj):
        level = obj.verification_level
        color = 'green' if level >= 80 else 'orange' if level >= 50 else 'red'
        return format_html(
            '<span style="color: {};">{:.1f}%</span>',
            color, level
        )
    verification_level.short_description = 'Verification Level'


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    """
    Admin interface for UserActivity model.
    """
    list_display = ['user', 'activity_type', 'ip_address', 'created_at']
    list_filter = ['activity_type', 'created_at']
    search_fields = ['user__email', 'user__username', 'ip_address']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    """
    Admin interface for EmailVerification model.
    """
    list_display = ['user', 'email', 'is_used', 'expires_at', 'created_at']
    list_filter = ['is_used', 'expires_at', 'created_at']
    search_fields = ['user__email', 'email', 'token']
    readonly_fields = ['token', 'created_at']


@admin.register(PhoneVerification)
class PhoneVerificationAdmin(admin.ModelAdmin):
    """
    Admin interface for PhoneVerification model.
    """
    list_display = ['user', 'phone_number', 'code', 'is_used', 'attempts', 'expires_at']
    list_filter = ['is_used', 'expires_at', 'created_at']
    search_fields = ['user__email', 'phone_number']
    readonly_fields = ['created_at']


@admin.register(UserPreferences)
class UserPreferencesAdmin(admin.ModelAdmin):
    """
    Admin interface for UserPreferences model.
    """
    list_display = ['user', 'email_new_messages', 'sms_new_messages', 'two_factor_enabled']
    search_fields = ['user__email', 'user__username']
    list_filter = ['email_new_messages', 'sms_new_messages', 'two_factor_enabled']