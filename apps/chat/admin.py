"""
Admin configuration for chat app.
"""
from django.contrib import admin
from .models import Conversation, Message, ChatBlock, ChatReport, PriceOffer


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    """
    Admin interface for Conversation model.
    """
    list_display = [
        'id', 'title', 'product', 'participant_list', 'is_active',
        'last_message_at', 'created_at'
    ]
    list_filter = ['is_active', 'is_archived', 'created_at', 'last_message_at']
    search_fields = ['title', 'product__title', 'participants__email']
    readonly_fields = ['created_at', 'updated_at']

    def participant_list(self, obj):
        return ', '.join([p.full_name for p in obj.participants.all()])
    participant_list.short_description = 'Participants'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """
    Admin interface for Message model.
    """
    list_display = [
        'id', 'conversation', 'sender', 'message_type', 'content_preview',
        'is_read', 'created_at'
    ]
    list_filter = ['message_type', 'is_read', 'is_edited', 'created_at']
    search_fields = ['content', 'sender__email', 'conversation__title']
    readonly_fields = ['created_at', 'updated_at']

    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'


@admin.register(PriceOffer)
class PriceOfferAdmin(admin.ModelAdmin):
    """
    Admin interface for PriceOffer model.
    """
    list_display = [
        'id', 'product', 'offerer', 'recipient', 'offered_price',
        'original_price', 'status', 'expires_at', 'created_at'
    ]
    list_filter = ['status', 'expires_at', 'created_at']
    search_fields = ['product__title', 'offerer__email', 'recipient__email']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ChatBlock)
class ChatBlockAdmin(admin.ModelAdmin):
    """
    Admin interface for ChatBlock model.
    """
    list_display = ['blocker', 'blocked', 'reason', 'created_at']
    search_fields = ['blocker__email', 'blocked__email', 'reason']
    readonly_fields = ['created_at']


@admin.register(ChatReport)
class ChatReportAdmin(admin.ModelAdmin):
    """
    Admin interface for ChatReport model.
    """
    list_display = [
        'reporter', 'reported_user', 'reason', 'is_resolved',
        'resolved_by', 'created_at'
    ]
    list_filter = ['reason', 'is_resolved', 'created_at']
    search_fields = ['reporter__email', 'reported_user__email', 'description']
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