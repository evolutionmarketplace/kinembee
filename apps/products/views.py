"""
Views for products.
"""
from rest_framework import generics, permissions, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count, Avg
from django.utils import timezone
from .models import Product, ProductWishlist, ProductReport, SavedSearch, ProductView
from .serializers import (
    ProductListSerializer, ProductDetailSerializer, ProductCreateUpdateSerializer,
    ProductWishlistSerializer, ProductReportSerializer, SavedSearchSerializer
)
from .filters import ProductFilter
from apps.core.permissions import IsSellerOrReadOnly, CanCreateListing
from apps.core.pagination import CustomPageNumberPagination
import logging

logger = logging.getLogger(__name__)


class ProductListView(generics.ListAPIView):
    """
    List products with filtering, searching, and sorting.
    """
    serializer_class = ProductListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['title', 'description', 'brand', 'model']
    ordering_fields = ['price', 'created_at', 'views', 'likes']
    ordering = ['-is_boosted', '-created_at']
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        return Product.objects.filter(
            is_active=True,
            status='active'
        ).select_related('seller', 'category').prefetch_related('images')


class ProductDetailView(generics.RetrieveAPIView):
    """
    Retrieve detailed product information.
    """
    serializer_class = ProductDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'

    def get_queryset(self):
        return Product.objects.filter(
            is_active=True
        ).select_related('seller', 'category', 'subcategory').prefetch_related('images')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Track view
        self.track_view(request, instance)
        
        # Increment view count
        instance.increment_views()
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def track_view(self, request, product):
        """Track product view for analytics."""
        ip_address = self.get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        ProductView.objects.create(
            product=product,
            user=request.user if request.user.is_authenticated else None,
            ip_address=ip_address,
            user_agent=user_agent
        )

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class ProductCreateView(generics.CreateAPIView):
    """
    Create a new product listing.
    """
    serializer_class = ProductCreateUpdateSerializer
    permission_classes = [CanCreateListing]

    def perform_create(self, serializer):
        product = serializer.save()
        
        # Log activity
        from apps.accounts.models import UserActivity
        UserActivity.objects.create(
            user=self.request.user,
            activity_type='listing_create',
            description=f"Created listing: {product.title}",
            metadata={'product_id': str(product.id)}
        )


class ProductUpdateView(generics.UpdateAPIView):
    """
    Update an existing product listing.
    """
    serializer_class = ProductCreateUpdateSerializer
    permission_classes = [IsSellerOrReadOnly]

    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user)


class ProductDeleteView(generics.DestroyAPIView):
    """
    Delete (soft delete) a product listing.
    """
    permission_classes = [IsSellerOrReadOnly]

    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()  # This will soft delete
        
        # Log activity
        from apps.accounts.models import UserActivity
        UserActivity.objects.create(
            user=self.request.user,
            activity_type='listing_delete',
            description=f"Deleted listing: {instance.title}",
            metadata={'product_id': str(instance.id)}
        )


class MyProductsView(generics.ListAPIView):
    """
    List current user's products.
    """
    serializer_class = ProductListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'price', 'views', 'status']
    ordering = ['-created_at']

    def get_queryset(self):
        return Product.objects.filter(
            seller=self.request.user
        ).select_related('category').prefetch_related('images')


class ProductWishlistView(generics.ListCreateAPIView):
    """
    List and manage user's wishlist.
    """
    serializer_class = ProductWishlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ProductWishlist.objects.filter(
            user=self.request.user
        ).select_related('product__seller', 'product__category')

    def create(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        try:
            product = Product.objects.get(id=product_id, is_active=True)
            wishlist_item, created = ProductWishlist.objects.get_or_create(
                user=request.user,
                product=product
            )
            
            if created:
                return Response({'message': 'Added to wishlist'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': 'Already in wishlist'}, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)


class ProductWishlistRemoveView(generics.DestroyAPIView):
    """
    Remove item from wishlist.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ProductWishlist.objects.filter(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id')
        try:
            wishlist_item = ProductWishlist.objects.get(
                user=request.user,
                product_id=product_id
            )
            wishlist_item.delete()
            return Response({'message': 'Removed from wishlist'}, status=status.HTTP_200_OK)
        except ProductWishlist.DoesNotExist:
            return Response({'error': 'Item not in wishlist'}, status=status.HTTP_404_NOT_FOUND)


class ProductReportView(generics.CreateAPIView):
    """
    Report a product.
    """
    serializer_class = ProductReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        try:
            product = Product.objects.get(id=self.kwargs['product_id'])
            context['product'] = product
        except Product.DoesNotExist:
            pass
        return context

    def create(self, request, *args, **kwargs):
        try:
            product = Product.objects.get(id=kwargs['product_id'])
            
            # Check if user already reported this product
            if ProductReport.objects.filter(
                product=product,
                reporter=request.user
            ).exists():
                return Response(
                    {'error': 'You have already reported this product'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            return super().create(request, *args, **kwargs)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)


class SavedSearchListView(generics.ListCreateAPIView):
    """
    List and create saved searches.
    """
    serializer_class = SavedSearchSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SavedSearch.objects.filter(user=self.request.user)


class SavedSearchDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a saved search.
    """
    serializer_class = SavedSearchSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SavedSearch.objects.filter(user=self.request.user)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def featured_products(request):
    """
    Get featured products for homepage.
    """
    products = Product.objects.filter(
        is_active=True,
        status='active',
        is_featured=True
    ).select_related('seller', 'category').prefetch_related('images')[:6]
    
    serializer = ProductListSerializer(products, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def trending_products(request):
    """
    Get trending products based on views and engagement.
    """
    # Get products with high engagement in the last week
    week_ago = timezone.now() - timezone.timedelta(days=7)
    
    products = Product.objects.filter(
        is_active=True,
        status='active',
        created_at__gte=week_ago
    ).annotate(
        engagement_score=Count('view_records') + Count('wishlisted_by') * 2
    ).order_by('-engagement_score')[:8]
    
    serializer = ProductListSerializer(products, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_as_sold(request, product_id):
    """
    Mark a product as sold.
    """
    try:
        product = Product.objects.get(
            id=product_id,
            seller=request.user,
            status='active'
        )
        
        buyer_email = request.data.get('buyer_email')
        buyer = None
        
        if buyer_email:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            try:
                buyer = User.objects.get(email=buyer_email)
            except User.DoesNotExist:
                pass
        
        product.mark_as_sold(buyer=buyer)
        
        return Response({'message': 'Product marked as sold'})
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def product_stats(request):
    """
    Get product statistics.
    """
    stats = {
        'total_products': Product.objects.filter(is_active=True).count(),
        'active_listings': Product.objects.filter(is_active=True, status='active').count(),
        'sold_products': Product.objects.filter(status='sold').count(),
        'featured_products': Product.objects.filter(is_active=True, is_featured=True).count(),
        'boosted_products': Product.objects.filter(is_active=True, is_boosted=True).count(),
    }
    
    return Response(stats)