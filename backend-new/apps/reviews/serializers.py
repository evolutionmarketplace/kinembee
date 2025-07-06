"""
Serializers for reviews.
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Review, ReviewImage, ReviewHelpful, ReviewResponse, ReviewReport
from apps.accounts.serializers import PublicUserSerializer
from apps.products.serializers import ProductListSerializer

User = get_user_model()


class ReviewImageSerializer(serializers.ModelSerializer):
    """
    Serializer for review images.
    """
    class Meta:
        model = ReviewImage
        fields = ['id', 'image', 'caption']


class ReviewResponseSerializer(serializers.ModelSerializer):
    """
    Serializer for review responses.
    """
    responder = PublicUserSerializer(read_only=True)

    class Meta:
        model = ReviewResponse
        fields = ['id', 'responder', 'response', 'created_at']


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for reviews.
    """
    reviewer = PublicUserSerializer(read_only=True)
    reviewee = PublicUserSerializer(read_only=True)
    product = ProductListSerializer(read_only=True)
    images = ReviewImageSerializer(many=True, read_only=True)
    response = ReviewResponseSerializer(read_only=True)
    is_helpful = serializers.SerializerMethodField()
    can_respond = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = [
            'id', 'reviewer', 'reviewee', 'product', 'review_type',
            'rating', 'title', 'comment', 'communication_rating',
            'delivery_rating', 'item_description_rating', 'is_verified',
            'is_featured', 'helpful_count', 'images', 'response',
            'created_at', 'is_helpful', 'can_respond'
        ]

    def get_is_helpful(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return ReviewHelpful.objects.filter(
                user=request.user,
                review=obj
            ).exists()
        return False

    def get_can_respond(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return (
                obj.reviewee == request.user and
                not hasattr(obj, 'response')
            )
        return False


class ReviewCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating reviews.
    """
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Review
        fields = [
            'product', 'reviewee', 'review_type', 'rating', 'title',
            'comment', 'communication_rating', 'delivery_rating',
            'item_description_rating', 'uploaded_images'
        ]

    def validate(self, attrs):
        request = self.context['request']
        product = attrs['product']
        reviewee = attrs['reviewee']
        
        # Check if user has already reviewed this product
        if Review.objects.filter(
            reviewer=request.user,
            product=product,
            review_type=attrs['review_type']
        ).exists():
            raise serializers.ValidationError("You have already reviewed this product.")
        
        # Check if user can review (has interacted with the product/seller)
        # This would typically check if there was a transaction
        
        return attrs

    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        validated_data['reviewer'] = self.context['request'].user
        
        review = Review.objects.create(**validated_data)
        
        # Handle image uploads
        for image in uploaded_images:
            ReviewImage.objects.create(
                review=review,
                image=image
            )
        
        return review


class ReviewResponseCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating review responses.
    """
    class Meta:
        model = ReviewResponse
        fields = ['response']

    def create(self, validated_data):
        validated_data['responder'] = self.context['request'].user
        validated_data['review'] = self.context['review']
        return ReviewResponse.objects.create(**validated_data)


class ReviewReportSerializer(serializers.ModelSerializer):
    """
    Serializer for review reports.
    """
    class Meta:
        model = ReviewReport
        fields = ['reason', 'description']

    def create(self, validated_data):
        validated_data['reporter'] = self.context['request'].user
        validated_data['review'] = self.context['review']
        return ReviewReport.objects.create(**validated_data)