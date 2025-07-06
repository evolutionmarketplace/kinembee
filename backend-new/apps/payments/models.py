"""
Payment models for Evolution Digital Market.
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from apps.core.models import TimeStampedModel
from apps.products.models import Product
import uuid

User = get_user_model()


class PaymentMethod(TimeStampedModel):
    """
    User payment methods.
    """
    PAYMENT_TYPES = [
        ('card', 'Credit/Debit Card'),
        ('paypal', 'PayPal'),
        ('bank', 'Bank Transfer'),
        ('crypto', 'Cryptocurrency'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_methods')
    payment_type = models.CharField(max_length=10, choices=PAYMENT_TYPES)
    
    # Card details (encrypted)
    card_last_four = models.CharField(max_length=4, blank=True)
    card_brand = models.CharField(max_length=20, blank=True)
    card_exp_month = models.PositiveIntegerField(null=True, blank=True)
    card_exp_year = models.PositiveIntegerField(null=True, blank=True)
    
    # External payment provider IDs
    stripe_payment_method_id = models.CharField(max_length=100, blank=True)
    paypal_email = models.EmailField(blank=True)
    
    # Status
    is_default = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'payment_methods'

    def __str__(self):
        if self.payment_type == 'card' and self.card_last_four:
            return f"{self.card_brand} ending in {self.card_last_four}"
        return f"{self.get_payment_type_display()}"

    def save(self, *args, **kwargs):
        # Ensure only one default payment method per user
        if self.is_default:
            PaymentMethod.objects.filter(
                user=self.user,
                is_default=True
            ).exclude(id=self.id).update(is_default=False)
        super().save(*args, **kwargs)


class Transaction(TimeStampedModel):
    """
    Financial transactions in the system.
    """
    TRANSACTION_TYPES = [
        ('boost_payment', 'Boost Payment'),
        ('commission', 'Commission'),
        ('refund', 'Refund'),
        ('withdrawal', 'Withdrawal'),
        ('deposit', 'Deposit'),
        ('fee', 'Platform Fee'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]

    # Transaction details
    transaction_id = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    
    # Amounts
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    fee_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    net_amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    
    # Status and timing
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    processed_at = models.DateTimeField(null=True, blank=True)
    
    # Payment details
    payment_method = models.ForeignKey(
        PaymentMethod, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    
    # External references
    stripe_payment_intent_id = models.CharField(max_length=100, blank=True)
    stripe_charge_id = models.CharField(max_length=100, blank=True)
    
    # Related objects
    product = models.ForeignKey(
        Product, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='transactions'
    )
    
    # Additional data
    description = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    
    # Failure information
    failure_reason = models.TextField(blank=True)
    failure_code = models.CharField(max_length=50, blank=True)
    
    class Meta:
        db_table = 'transactions'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['transaction_type', 'status']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.transaction_id} - {self.user.email} - ${self.amount}"

    def save(self, *args, **kwargs):
        if not self.transaction_id:
            self.transaction_id = f"TXN_{uuid.uuid4().hex[:12].upper()}"
        
        # Calculate net amount
        self.net_amount = self.amount - self.fee_amount
        
        super().save(*args, **kwargs)


class BoostPackage(TimeStampedModel):
    """
    Boost packages for product listings.
    """
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    duration_days = models.PositiveIntegerField()
    
    # Features
    priority_placement = models.BooleanField(default=True)
    featured_badge = models.BooleanField(default=True)
    social_media_promotion = models.BooleanField(default=False)
    email_newsletter_inclusion = models.BooleanField(default=False)
    
    # Visibility
    is_active = models.BooleanField(default=True)
    is_popular = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField(default=0)
    
    class Meta:
        db_table = 'boost_packages'
        ordering = ['sort_order', 'price']

    def __str__(self):
        return f"{self.name} - ${self.price} for {self.duration_days} days"


class ProductBoost(TimeStampedModel):
    """
    Product boost purchases and tracking.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='boosts')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_boosts')
    package = models.ForeignKey(BoostPackage, on_delete=models.CASCADE)
    transaction = models.OneToOneField(
        Transaction, 
        on_delete=models.CASCADE,
        related_name='product_boost'
    )
    
    # Timing
    starts_at = models.DateTimeField()
    expires_at = models.DateTimeField()
    
    # Status
    is_active = models.BooleanField(default=True)
    
    # Analytics
    impressions = models.PositiveIntegerField(default=0)
    clicks = models.PositiveIntegerField(default=0)
    
    class Meta:
        db_table = 'product_boosts'
        ordering = ['-created_at']

    def __str__(self):
        return f"Boost for {self.product.title} - {self.package.name}"

    @property
    def is_expired(self):
        from django.utils import timezone
        return timezone.now() > self.expires_at

    @property
    def click_through_rate(self):
        if self.impressions > 0:
            return (self.clicks / self.impressions) * 100
        return 0


class Wallet(TimeStampedModel):
    """
    User wallet for storing credits and managing payouts.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    
    # Balances
    available_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pending_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_earned = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_withdrawn = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Settings
    auto_withdraw_enabled = models.BooleanField(default=False)
    auto_withdraw_threshold = models.DecimalField(max_digits=8, decimal_places=2, default=100)
    
    class Meta:
        db_table = 'wallets'

    def __str__(self):
        return f"Wallet for {self.user.email} - ${self.available_balance}"

    def add_funds(self, amount, description=""):
        """Add funds to available balance."""
        self.available_balance += amount
        self.total_earned += amount
        self.save()
        
        # Create transaction record
        Transaction.objects.create(
            user=self.user,
            transaction_type='deposit',
            amount=amount,
            net_amount=amount,
            status='completed',
            description=description
        )

    def withdraw_funds(self, amount, payment_method=None):
        """Withdraw funds from wallet."""
        if amount > self.available_balance:
            raise ValueError("Insufficient funds")
        
        self.available_balance -= amount
        self.total_withdrawn += amount
        self.save()
        
        # Create withdrawal transaction
        return Transaction.objects.create(
            user=self.user,
            transaction_type='withdrawal',
            amount=amount,
            net_amount=amount,
            status='pending',
            payment_method=payment_method,
            description=f"Withdrawal to {payment_method}"
        )


class Invoice(TimeStampedModel):
    """
    Invoices for transactions and payments.
    """
    invoice_number = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invoices')
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, related_name='invoice')
    
    # Invoice details
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Billing information
    billing_name = models.CharField(max_length=200)
    billing_email = models.EmailField()
    billing_address = models.TextField()
    
    # Status
    is_paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'invoices'
        ordering = ['-created_at']

    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.user.email}"

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            from datetime import datetime
            self.invoice_number = f"INV-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)