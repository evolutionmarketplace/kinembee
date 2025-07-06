"""
Serializers for chat.
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Conversation, Message, PriceOffer, ChatReport
from apps.accounts.serializers import PublicUserSerializer
from apps.products.serializers import ProductListSerializer

User = get_user_model()


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for messages.
    """
    sender = PublicUserSerializer(read_only=True)
    time_ago = serializers.SerializerMethodField()
    attachment_url = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = [
            'id', 'sender', 'message_type', 'content', 'attachment',
            'attachment_name', 'attachment_size', 'attachment_url',
            'is_read', 'read_at', 'is_edited', 'edited_at',
            'metadata', 'created_at', 'time_ago'
        ]

    def get_time_ago(self, obj):
        from django.utils import timezone
        from datetime import timedelta
        
        now = timezone.now()
        diff = now - obj.created_at
        
        if diff < timedelta(minutes=1):
            return "Just now"
        elif diff < timedelta(hours=1):
            return f"{diff.seconds // 60}m ago"
        elif diff < timedelta(days=1):
            return f"{diff.seconds // 3600}h ago"
        else:
            return obj.created_at.strftime("%b %d, %H:%M")

    def get_attachment_url(self, obj):
        if obj.attachment:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.attachment.url)
        return None


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for conversations.
    """
    participants = PublicUserSerializer(many=True, read_only=True)
    product = ProductListSerializer(read_only=True)
    last_message_preview = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()
    other_participant = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            'id', 'participants', 'product', 'title', 'is_active',
            'last_message_at', 'last_message_preview', 'unread_count',
            'other_participant', 'created_at'
        ]

    def get_last_message_preview(self, obj):
        if obj.last_message:
            return obj.last_message[:100] + "..." if len(obj.last_message) > 100 else obj.last_message
        return ""

    def get_unread_count(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.get_unread_count(request.user)
        return 0

    def get_other_participant(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            other = obj.other_participant(request.user)
            if other:
                return PublicUserSerializer(other).data
        return None


class MessageCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating messages.
    """
    class Meta:
        model = Message
        fields = ['content', 'message_type', 'attachment', 'metadata']

    def create(self, validated_data):
        validated_data['sender'] = self.context['request'].user
        validated_data['conversation'] = self.context['conversation']
        
        message = Message.objects.create(**validated_data)
        
        # Update conversation last message
        conversation = message.conversation
        conversation.last_message = message.content
        conversation.last_message_at = message.created_at
        conversation.save()
        
        return message


class PriceOfferSerializer(serializers.ModelSerializer):
    """
    Serializer for price offers.
    """
    offerer = PublicUserSerializer(read_only=True)
    recipient = PublicUserSerializer(read_only=True)
    product = ProductListSerializer(read_only=True)
    is_expired = serializers.ReadOnlyField()
    discount_percentage = serializers.ReadOnlyField()

    class Meta:
        model = PriceOffer
        fields = [
            'id', 'offerer', 'recipient', 'product', 'offered_price',
            'original_price', 'status', 'expires_at', 'response_message',
            'responded_at', 'is_expired', 'discount_percentage', 'created_at'
        ]


class PriceOfferCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating price offers.
    """
    class Meta:
        model = PriceOffer
        fields = ['offered_price']

    def validate_offered_price(self, value):
        product = self.context['product']
        if value <= 0:
            raise serializers.ValidationError("Offer price must be greater than 0.")
        if value >= product.price:
            raise serializers.ValidationError("Offer price must be less than the listing price.")
        return value

    def create(self, validated_data):
        from django.utils import timezone
        from datetime import timedelta
        
        conversation = self.context['conversation']
        product = self.context['product']
        user = self.context['request'].user
        
        # Create the message first
        message = Message.objects.create(
            conversation=conversation,
            sender=user,
            message_type='offer',
            content=f"Price offer: ${validated_data['offered_price']}"
        )
        
        # Create the price offer
        offer = PriceOffer.objects.create(
            conversation=conversation,
            product=product,
            message=message,
            offerer=user,
            recipient=product.seller,
            offered_price=validated_data['offered_price'],
            original_price=product.price,
            expires_at=timezone.now() + timedelta(days=3)
        )
        
        return offer


class ChatReportSerializer(serializers.ModelSerializer):
    """
    Serializer for chat reports.
    """
    class Meta:
        model = ChatReport
        fields = ['reason', 'description']

    def create(self, validated_data):
        validated_data['reporter'] = self.context['request'].user
        validated_data['conversation'] = self.context['conversation']
        validated_data['reported_user'] = self.context['reported_user']
        return ChatReport.objects.create(**validated_data)


class ConversationCreateSerializer(serializers.Serializer):
    """
    Serializer for creating conversations.
    """
    product_id = serializers.UUIDField()
    message = serializers.CharField(max_length=1000)

    def validate_product_id(self, value):
        from apps.products.models import Product
        try:
            product = Product.objects.get(id=value, is_active=True)
            if product.seller == self.context['request'].user:
                raise serializers.ValidationError("You cannot message yourself about your own product.")
            return value
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product not found.")

    def create(self, validated_data):
        from apps.products.models import Product
        
        user = self.context['request'].user
        product = Product.objects.get(id=validated_data['product_id'])
        
        # Check if conversation already exists
        existing_conversation = Conversation.objects.filter(
            participants=user,
            product=product
        ).filter(participants=product.seller).first()
        
        if existing_conversation:
            conversation = existing_conversation
        else:
            # Create new conversation
            conversation = Conversation.objects.create(
                product=product,
                title=f"About {product.title}"
            )
            conversation.participants.add(user, product.seller)
        
        # Create initial message
        Message.objects.create(
            conversation=conversation,
            sender=user,
            content=validated_data['message']
        )
        
        return conversation