"""
Chat models for Evolution Digital Market.
"""
from django.db import models
from django.contrib.auth import get_user_model
from apps.core.models import TimeStampedModel
from apps.products.models import Product
import uuid

User = get_user_model()


class Conversation(TimeStampedModel):
    """
    Chat conversations between users.
    """
    participants = models.ManyToManyField(User, related_name='conversations')
    product = models.ForeignKey(
        Product, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='conversations'
    )
    
    # Conversation metadata
    title = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    is_archived = models.BooleanField(default=False)
    
    # Last activity tracking
    last_message_at = models.DateTimeField(null=True, blank=True)
    last_message = models.TextField(blank=True)
    
    class Meta:
        db_table = 'conversations'
        ordering = ['-last_message_at', '-created_at']

    def __str__(self):
        participant_names = ', '.join([p.full_name for p in self.participants.all()[:2]])
        return f"Conversation: {participant_names}"

    @property
    def other_participant(self, current_user):
        """Get the other participant in a 2-person conversation."""
        return self.participants.exclude(id=current_user.id).first()

    def get_unread_count(self, user):
        """Get unread message count for a specific user."""
        return self.messages.filter(is_read=False).exclude(sender=user).count()


class Message(TimeStampedModel):
    """
    Individual messages in conversations.
    """
    MESSAGE_TYPES = [
        ('text', 'Text'),
        ('image', 'Image'),
        ('file', 'File'),
        ('system', 'System'),
        ('offer', 'Price Offer'),
    ]

    conversation = models.ForeignKey(
        Conversation, 
        on_delete=models.CASCADE, 
        related_name='messages'
    )
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    
    # Message content
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPES, default='text')
    content = models.TextField()
    
    # File attachments
    attachment = models.FileField(upload_to='chat/attachments/', blank=True, null=True)
    attachment_name = models.CharField(max_length=255, blank=True)
    attachment_size = models.PositiveIntegerField(null=True, blank=True)
    
    # Message status
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    is_edited = models.BooleanField(default=False)
    edited_at = models.DateTimeField(null=True, blank=True)
    
    # Special message data (for offers, etc.)
    metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        db_table = 'messages'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['conversation', 'created_at']),
            models.Index(fields=['sender', 'created_at']),
            models.Index(fields=['is_read']),
        ]

    def __str__(self):
        return f"Message from {self.sender.full_name} in {self.conversation.id}"

    def mark_as_read(self, user=None):
        """Mark message as read."""
        if not self.is_read and (user is None or self.sender != user):
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=['is_read', 'read_at'])


class MessageRead(TimeStampedModel):
    """
    Track which users have read which messages.
    """
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='read_receipts')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    read_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'message_reads'
        unique_together = ['message', 'user']

    def __str__(self):
        return f"{self.user.full_name} read message {self.message.id}"


class ChatBlock(TimeStampedModel):
    """
    Users blocking other users from messaging.
    """
    blocker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocked_users')
    blocked = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocked_by')
    reason = models.TextField(blank=True)

    class Meta:
        db_table = 'chat_blocks'
        unique_together = ['blocker', 'blocked']

    def __str__(self):
        return f"{self.blocker.full_name} blocked {self.blocked.full_name}"


class ChatReport(TimeStampedModel):
    """
    Reports for inappropriate chat behavior.
    """
    REPORT_REASONS = [
        ('spam', 'Spam'),
        ('harassment', 'Harassment'),
        ('inappropriate', 'Inappropriate Content'),
        ('scam', 'Scam/Fraud'),
        ('fake', 'Fake Profile'),
        ('other', 'Other'),
    ]

    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_reports')
    reported_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_in_chat')
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='reports')
    message = models.ForeignKey(
        Message, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='reports'
    )
    
    reason = models.CharField(max_length=20, choices=REPORT_REASONS)
    description = models.TextField(blank=True)
    
    # Resolution
    is_resolved = models.BooleanField(default=False)
    resolved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='resolved_chat_reports'
    )
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolution_notes = models.TextField(blank=True)

    class Meta:
        db_table = 'chat_reports'

    def __str__(self):
        return f"Report by {self.reporter.full_name} against {self.reported_user.full_name}"


class PriceOffer(TimeStampedModel):
    """
    Price offers made through chat.
    """
    OFFER_STATUS = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
        ('countered', 'Countered'),
        ('expired', 'Expired'),
    ]

    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='offers')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='offers')
    message = models.OneToOneField(Message, on_delete=models.CASCADE, related_name='price_offer')
    
    # Offer details
    offerer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='offers_made')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='offers_received')
    
    offered_price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Status and timing
    status = models.CharField(max_length=10, choices=OFFER_STATUS, default='pending')
    expires_at = models.DateTimeField()
    
    # Response
    response_message = models.TextField(blank=True)
    responded_at = models.DateTimeField(null=True, blank=True)
    
    # Counter offer
    counter_offer = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='original_offer'
    )

    class Meta:
        db_table = 'price_offers'
        ordering = ['-created_at']

    def __str__(self):
        return f"Offer: ${self.offered_price} for {self.product.title}"

    @property
    def is_expired(self):
        from django.utils import timezone
        return timezone.now() > self.expires_at

    @property
    def discount_percentage(self):
        if self.original_price > 0:
            return ((self.original_price - self.offered_price) / self.original_price) * 100
        return 0

    def accept(self, response_message=""):
        """Accept the offer."""
        self.status = 'accepted'
        self.response_message = response_message
        self.responded_at = timezone.now()
        self.save()

    def decline(self, response_message=""):
        """Decline the offer."""
        self.status = 'declined'
        self.response_message = response_message
        self.responded_at = timezone.now()
        self.save()

    def counter(self, new_price, response_message=""):
        """Create a counter offer."""
        self.status = 'countered'
        self.response_message = response_message
        self.responded_at = timezone.now()
        self.save()
        
        # Create counter offer
        counter_offer = PriceOffer.objects.create(
            conversation=self.conversation,
            product=self.product,
            offerer=self.recipient,
            recipient=self.offerer,
            offered_price=new_price,
            original_price=self.original_price,
            expires_at=timezone.now() + timezone.timedelta(days=3),
            counter_offer=self
        )
        
        return counter_offer