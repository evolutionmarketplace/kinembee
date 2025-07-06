"""
Admin configuration for payments app.
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import (
    PaymentMethod, Transaction, BoostPackage, ProductBoost, 
    Wallet, Invoice
)


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    """
    Admin interface for PaymentMethod model.
    """
    list_display = [
        'user', 'payment_type', 'card_display', 'is_default',
        'is_verified', 'is_active', 'created_at'
    ]
    list_filter = ['payment_type', 'is_default', 'is_verified', 'is_active']
    search_fields = ['user__email', 'card_last_four', 'paypal_email']

    def card_display(self, obj):
        if obj.payment_type == 'card' and obj.card_last_four:
            return f"{obj.card_brand} •••• {obj.card_last_four}"
        return '-'
    card_display.short_description = 'Card Info'


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """
    Admin interface for Transaction model.
    """
    list_display = [
        'transaction_id', 'user', 'transaction_type', 'amount',
        'status', 'created_at', 'processed_at'
    ]
    list_filter = ['transaction_type', 'status', 'created_at']
    search_fields = ['transaction_id', 'user__email', 'stripe_payment_intent_id']
    readonly_fields = ['transaction_id', 'created_at', 'updated_at']

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing existing object
            return self.readonly_fields + ['user', 'amount', 'transaction_type']
        return self.readonly_fields


@admin.register(BoostPackage)
class BoostPackageAdmin(admin.ModelAdmin):
    """
    Admin interface for BoostPackage model.
    """
    list_display = [
        'name', 'price', 'duration_days', 'is_active',
        'is_popular', 'sort_order'
    ]
    list_filter = ['is_active', 'is_popular']
    search_fields = ['name', 'description']
    ordering = ['sort_order', 'price']


@admin.register(ProductBoost)
class ProductBoostAdmin(admin.ModelAdmin):
    """
    Admin interface for ProductBoost model.
    """
    list_display = [
        'product', 'user', 'package', 'starts_at', 'expires_at',
        'is_active', 'impressions', 'clicks', 'ctr'
    ]
    list_filter = ['is_active', 'package', 'starts_at', 'expires_at']
    search_fields = ['product__title', 'user__email']
    readonly_fields = ['impressions', 'clicks', 'ctr']

    def ctr(self, obj):
        return f"{obj.click_through_rate:.2f}%"
    ctr.short_description = 'CTR'


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    """
    Admin interface for Wallet model.
    """
    list_display = [
        'user', 'available_balance', 'pending_balance',
        'total_earned', 'total_withdrawn', 'auto_withdraw_enabled'
    ]
    search_fields = ['user__email']
    readonly_fields = ['total_earned', 'total_withdrawn']


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    """
    Admin interface for Invoice model.
    """
    list_display = [
        'invoice_number', 'user', 'total_amount', 'is_paid',
        'created_at', 'paid_at'
    ]
    list_filter = ['is_paid', 'created_at', 'paid_at']
    search_fields = ['invoice_number', 'user__email', 'billing_email']
    readonly_fields = ['invoice_number', 'created_at']