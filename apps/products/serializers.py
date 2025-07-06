"""
Serializers for products.
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Product, ProductImage, ProductWishlist, ProductReport, SavedSearch
from apps.accounts.serializers import PublicUserSerializer
from apps.categories.serializers import CategoryListSerializer

User = get_user_model()


class ProductImageSerializer(serializers.ModelSerializer):
    """
    Serializer for product images.
    """
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'thumbnail', 'alt_text', 'is_primary', 'sort_order']


class ProductListSerializer(serializers.ModelSerializer):
    """
    Serializer for product list views.
    """
    seller = PublicUserSerializer(read_only=True)
    category = CategoryListSerializer(read_only=True)
    main_image = ProductImageSerializer(read_only=True)
    is_wishlisted = serializers.SerializerMethodField()
    distance = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'title', 'slug', 'price', 'condition', 'location',
            'seller', 'category', 'main_image', 'views', 'likes',
            'is_boosted', 'is_featured', 'created_at', 'is_wishlisted',
            'distance'
        ]

    def get_is_wishlisted(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return ProductWishlist.objects.filter(
                user=request.user,
                product=obj
            ).exists()
        return False

    def get_distance(self, obj):
        # This would be calculated based on user's location
        # For now, return None
        return None


class ProductDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed product view.
    """
    seller = PublicUserSerializer(read_only=True)
    category = CategoryListSerializer(read_only=True)
    subcategory = CategoryListSerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    is_wishlisted = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    related_products = serializers.SerializerMethodField()
    tags_list = serializers.StringRelatedField(source='tags', many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'title', 'slug', 'description', 'price', 'condition',
            'brand', 'model', 'category', 'subcategory', 'seller',
            'location', 'pickup_available', 'delivery_available',
            'shipping_cost', 'status', 'is_active', 'is_featured',
            'is_boosted', 'views', 'likes', 'shares', 'images',
            'attributes', 'tags_list', 'created_at', 'updated_at',
            'is_wishlisted', 'is_owner', 'related_products'
        ]

    def get_is_wishlisted(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return ProductWishlist.objects.filter(
                user=request.user,
                product=obj
            ).exists()
        return False

    def get_is_owner(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.seller == request.user
        return False

    def get_related_products(self, obj):
        related = Product.objects.filter(
            category=obj.category,
            is_active=True,
            status='active'
        ).exclude(id=obj.id)[:4]
        
        return ProductListSerializer(
            related,
            many=True,
            context=self.context
        ).data


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating products.
    """
    images = ProductImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Product
        fields = [
            'title', 'description', 'price', 'condition', 'brand', 'model',
            'category', 'subcategory', 'location', 'pickup_available',
            'delivery_available', 'shipping_cost', 'attributes',
            'images', 'uploaded_images'
        ]

    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        validated_data['seller'] = self.context['request'].user
        product = Product.objects.create(**validated_data)
        
        # Handle image uploads
        for i, image in enumerate(uploaded_images):
            ProductImage.objects.create(
                product=product,
                image=image,
                is_primary=(i == 0),
                sort_order=i
            )
        
        return product

    def update(self, instance, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        
        # Update product fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Handle new image uploads
        if uploaded_images:
            existing_count = instance.images.count()
            for i, image in enumerate(uploaded_images):
                ProductImage.objects.create(
                    product=instance,
                    image=image,
                    is_primary=(existing_count == 0 and i == 0),
                    sort_order=existing_count + i
                )
        
        return instance


class ProductWishlistSerializer(serializers.ModelSerializer):
    """
    Serializer for wishlist items.
    """
    product = ProductListSerializer(read_only=True)

    class Meta:
        model = ProductWishlist
        fields = ['id', 'product', 'created_at']


class ProductReportSerializer(serializers.ModelSerializer):
    """
    Serializer for product reports.
    """
    class Meta:
        model = ProductReport
        fields = ['reason', 'description']

    def create(self, validated_data):
        validated_data['reporter'] = self.context['request'].user
        validated_data['product'] = self.context['product']
        return ProductReport.objects.create(**validated_data)


class SavedSearchSerializer(serializers.ModelSerializer):
    """
    Serializer for saved searches.
    """
    result_count = serializers.SerializerMethodField()

    class Meta:
        model = SavedSearch
        fields = [
            'id', 'name', 'query', 'filters', 'is_active',
            'email_alerts', 'result_count', 'created_at'
        ]

    def get_result_count(self, obj):
        # This would run the search query and return count
        # For now, return 0
        return 0

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return SavedSearch.objects.create(**validated_data)