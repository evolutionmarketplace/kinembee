"""
Serializers for payments.
"""
from rest_framework import serializers
from .models import PaymentMethod, Transaction, BoostPackage, ProductBoost, Wallet


class PaymentMethodSerializer(serializers.ModelSerializer):
    """
    Serializer for payment methods.
    """
    display_name = serializers.SerializerMethodField()

    class Meta:
        model = PaymentMethod
        fields = [
            'id', 'payment_type', 'card_last_four', 'card_brand',
            'card_exp_month', 'card_exp_year', 'is_default', 'is_verified',
            'display_name', 'created_at'
        ]
        read_only_fields = ['card_last_four', 'card_brand', 'is_verified']

    def get_display_name(self, obj):
        if obj.payment_type == 'card' and obj.card_last_four:
            return f"{obj.card_brand} •••• {obj.card_last_four}"
        return obj.get_payment_type_display()


class TransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for transactions.
    """
    payment_method_display = serializers.CharField(source='payment_method.display_name', read_only=True)
    product_title = serializers.CharField(source='product.title', read_only=True)

    class Meta:
        model = Transaction
        fields = [
            'id', 'transaction_id', 'transaction_type', 'amount', 'fee_amount',
            'net_amount', 'currency', 'status', 'description', 'created_at',
            'processed_at', 'payment_method_display', 'product_title'
        ]


class BoostPackageSerializer(serializers.ModelSerializer):
    """
    Serializer for boost packages.
    """
    features = serializers.SerializerMethodField()

    class Meta:
        model = BoostPackage
        fields = [
            'id', 'name', 'description', 'price', 'duration_days',
            'is_popular', 'features'
        ]

    def get_features(self, obj):
        features = []
        if obj.priority_placement:
            features.append('Priority Placement')
        if obj.featured_badge:
            features.append('Featured Badge')
        if obj.social_media_promotion:
            features.append('Social Media Promotion')
        if obj.email_newsletter_inclusion:
            features.append('Email Newsletter')
        return features


class ProductBoostSerializer(serializers.ModelSerializer):
    """
    Serializer for product boosts.
    """
    package = BoostPackageSerializer(read_only=True)
    product_title = serializers.CharField(source='product.title', read_only=True)
    is_expired = serializers.ReadOnlyField()
    click_through_rate = serializers.ReadOnlyField()

    class Meta:
        model = ProductBoost
        fields = [
            'id', 'product_title', 'package', 'starts_at', 'expires_at',
            'is_active', 'is_expired', 'impressions', 'clicks',
            'click_through_rate', 'created_at'
        ]


class WalletSerializer(serializers.ModelSerializer):
    """
    Serializer for wallet.
    """
    class Meta:
        model = Wallet
        fields = [
            'available_balance', 'pending_balance', 'total_earned',
            'total_withdrawn', 'auto_withdraw_enabled', 'auto_withdraw_threshold'
        ]


class BoostPurchaseSerializer(serializers.Serializer):
    """
    Serializer for boost purchase.
    """
    product_id = serializers.UUIDField()
    package_id = serializers.UUIDField()
    payment_method_id = serializers.UUIDField()

    def validate_product_id(self, value):
        from apps.products.models import Product
        try:
            product = Product.objects.get(id=value, seller=self.context['request'].user)
            return value
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product not found or you don't own it.")

    def validate_package_id(self, value):
        try:
            package = BoostPackage.objects.get(id=value, is_active=True)
            return value
        except BoostPackage.DoesNotExist:
            raise serializers.ValidationError("Boost package not found.")

    def validate_payment_method_id(self, value):
        try:
            payment_method = PaymentMethod.objects.get(
                id=value, 
                user=self.context['request'].user,
                is_active=True
            )
            return value
        except PaymentMethod.DoesNotExist:
            raise serializers.ValidationError("Payment method not found.")