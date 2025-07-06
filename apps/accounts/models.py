"""
User and authentication models for Evolution Digital Market.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from apps.core.models import TimeStampedModel, Address
import uuid


class User(AbstractUser):
    """
    Custom user model for Evolution Digital Market.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
        )]
    )
    
    # Profile fields
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    
    # Verification and status
    is_verified = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
    ban_reason = models.TextField(blank=True)
    banned_until = models.DateTimeField(blank=True, null=True)
    
    # Business account
    is_business = models.BooleanField(default=False)
    business_name = models.CharField(max_length=255, blank=True)
    business_license = models.CharField(max_length=100, blank=True)
    
    # Preferences
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    marketing_emails = models.BooleanField(default=True)
    
    # Location
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login_ip = models.GenericIPAddressField(blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username

    @property
    def is_active_user(self):
        """Check if user is active and not banned."""
        if self.is_banned:
            if self.banned_until and self.banned_until > timezone.now():
                return False
            elif not self.banned_until:  # Permanent ban
                return False
        return self.is_active

    def ban_user(self, reason, duration_days=None):
        """Ban user with optional duration."""
        self.is_banned = True
        self.ban_reason = reason
        if duration_days:
            self.banned_until = timezone.now() + timezone.timedelta(days=duration_days)
        self.save()

    def unban_user(self):
        """Remove ban from user."""
        self.is_banned = False
        self.ban_reason = ''
        self.banned_until = None
        self.save()


class UserProfile(TimeStampedModel):
    """
    Extended user profile information.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Social media links
    website = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    
    # Seller information
    seller_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_sales = models.PositiveIntegerField(default=0)
    total_reviews = models.PositiveIntegerField(default=0)
    response_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    response_time_hours = models.PositiveIntegerField(default=24)
    
    # Buyer information
    total_purchases = models.PositiveIntegerField(default=0)
    
    # Verification documents
    id_document = models.FileField(upload_to='verification/ids/', blank=True, null=True)
    address_proof = models.FileField(upload_to='verification/address/', blank=True, null=True)
    business_license_doc = models.FileField(upload_to='verification/business/', blank=True, null=True)
    
    # Verification status
    id_verified = models.BooleanField(default=False)
    address_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    business_verified = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'user_profiles'

    def __str__(self):
        return f"{self.user.email} Profile"

    @property
    def verification_level(self):
        """Calculate verification level percentage."""
        verifications = [
            self.email_verified,
            self.phone_verified,
            self.id_verified,
            self.address_verified,
        ]
        if self.user.is_business:
            verifications.append(self.business_verified)
        
        verified_count = sum(verifications)
        total_count = len(verifications)
        return (verified_count / total_count) * 100 if total_count > 0 else 0


class EmailVerification(TimeStampedModel):
    """
    Email verification tokens.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=64, unique=True)
    email = models.EmailField()
    is_used = models.BooleanField(default=False)
    expires_at = models.DateTimeField()

    class Meta:
        db_table = 'email_verifications'

    def __str__(self):
        return f"Email verification for {self.email}"

    @property
    def is_expired(self):
        return timezone.now() > self.expires_at

    @property
    def is_valid(self):
        return not self.is_used and not self.is_expired


class PhoneVerification(TimeStampedModel):
    """
    Phone number verification codes.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    code = models.CharField(max_length=6)
    is_used = models.BooleanField(default=False)
    expires_at = models.DateTimeField()
    attempts = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'phone_verifications'

    def __str__(self):
        return f"Phone verification for {self.phone_number}"

    @property
    def is_expired(self):
        return timezone.now() > self.expires_at

    @property
    def is_valid(self):
        return not self.is_used and not self.is_expired and self.attempts < 3


class UserActivity(TimeStampedModel):
    """
    Track user activities for analytics and security.
    """
    ACTIVITY_TYPES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('register', 'Register'),
        ('password_change', 'Password Change'),
        ('profile_update', 'Profile Update'),
        ('listing_create', 'Listing Created'),
        ('listing_update', 'Listing Updated'),
        ('listing_delete', 'Listing Deleted'),
        ('message_sent', 'Message Sent'),
        ('review_posted', 'Review Posted'),
        ('payment_made', 'Payment Made'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    description = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = 'user_activities'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.get_activity_type_display()}"


class UserPreferences(TimeStampedModel):
    """
    User preferences and settings.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preferences')
    
    # Notification preferences
    email_new_messages = models.BooleanField(default=True)
    email_listing_updates = models.BooleanField(default=True)
    email_price_alerts = models.BooleanField(default=True)
    email_marketing = models.BooleanField(default=True)
    
    sms_new_messages = models.BooleanField(default=False)
    sms_listing_updates = models.BooleanField(default=False)
    sms_security_alerts = models.BooleanField(default=True)
    
    push_new_messages = models.BooleanField(default=True)
    push_listing_updates = models.BooleanField(default=True)
    push_price_alerts = models.BooleanField(default=True)
    
    # Privacy preferences
    show_phone_number = models.BooleanField(default=True)
    show_email = models.BooleanField(default=False)
    show_last_seen = models.BooleanField(default=True)
    allow_contact_from_buyers = models.BooleanField(default=True)
    
    # Search and display preferences
    default_search_radius = models.PositiveIntegerField(default=50)  # kilometers
    preferred_currency = models.CharField(max_length=3, default='USD')
    preferred_language = models.CharField(max_length=5, default='en')
    items_per_page = models.PositiveIntegerField(default=20)
    
    # Security preferences
    two_factor_enabled = models.BooleanField(default=False)
    login_notifications = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'user_preferences'

    def __str__(self):
        return f"{self.user.email} Preferences"