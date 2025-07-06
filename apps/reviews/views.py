"""
Views for reviews.
"""
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg, Count
from .models import Review, ReviewHelpful, ReviewResponse, ReviewReport
from .serializers import (
    ReviewSerializer, ReviewCreateSerializer, ReviewResponseCreateSerializer,
    ReviewReportSerializer
)
from apps.products.models import Product
from apps.core.pagination import CustomPageNumberPagination
import logging

logger = logging.getLogger(__name__)


class ReviewListView(generics.ListAPIView):
    """
    List reviews with filtering options.
    """
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_type', 'rating', 'is_verified', 'is_featured']
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        queryset = Review.objects.select_related(
            'reviewer', 'reviewee', 'product'
        ).prefetch_related('images', 'response')
        
        # Filter by product
        product_id = self.request.query_params.get('product')
        if product_id:
            queryset = queryset.filter(product_id=product_id)
        
        # Filter by user (reviews received)
        user_id = self.request.query_params.get('user')
        if user_id:
            queryset = queryset.filter(reviewee_id=user_id)
        
        return queryset.order_by('-created_at')


class ReviewCreateView(generics.CreateAPIView):
    """
    Create a new review.
    """
    serializer_class = ReviewCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        review = serializer.save()
        
        # Log activity
        from apps.accounts.models import UserActivity
        UserActivity.objects.create(
            user=self.request.user,
            activity_type='review_posted',
            description=f"Posted review for {review.product.title}",
            metadata={'review_id': str(review.id)}
        )


class ReviewDetailView(generics.RetrieveAPIView):
    """
    Retrieve a specific review.
    """
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Review.objects.select_related(
        'reviewer', 'reviewee', 'product'
    ).prefetch_related('images', 'response')


class MyReviewsView(generics.ListAPIView):
    """
    List current user's reviews (given and received).
    """
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        review_type = self.request.query_params.get('type', 'given')
        
        if review_type == 'received':
            return Review.objects.filter(reviewee=user).select_related(
                'reviewer', 'product'
            ).prefetch_related('images', 'response')
        else:
            return Review.objects.filter(reviewer=user).select_related(
                'reviewee', 'product'
            ).prefetch_related('images', 'response')


class ReviewHelpfulView(APIView):
    """
    Mark a review as helpful or remove helpful mark.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, review_id):
        try:
            review = Review.objects.get(id=review_id)
            helpful, created = ReviewHelpful.objects.get_or_create(
                user=request.user,
                review=review
            )
            
            if created:
                # Increment helpful count
                review.helpful_count += 1
                review.save(update_fields=['helpful_count'])
                return Response({'message': 'Marked as helpful', 'helpful': True})
            else:
                # Remove helpful mark
                helpful.delete()
                review.helpful_count = max(0, review.helpful_count - 1)
                review.save(update_fields=['helpful_count'])
                return Response({'message': 'Removed helpful mark', 'helpful': False})
                
        except Review.DoesNotExist:
            return Response({'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)


class ReviewResponseView(generics.CreateAPIView):
    """
    Create a response to a review.
    """
    serializer_class = ReviewResponseCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        try:
            review = Review.objects.get(id=self.kwargs['review_id'])
            context['review'] = review
        except Review.DoesNotExist:
            pass
        return context

    def create(self, request, *args, **kwargs):
        try:
            review = Review.objects.get(id=kwargs['review_id'])
            
            # Check if user is the reviewee
            if review.reviewee != request.user:
                return Response(
                    {'error': 'You can only respond to reviews about you'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Check if response already exists
            if hasattr(review, 'response'):
                return Response(
                    {'error': 'Response already exists for this review'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            return super().create(request, *args, **kwargs)
        except Review.DoesNotExist:
            return Response({'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)


class ReviewReportView(generics.CreateAPIView):
    """
    Report a review.
    """
    serializer_class = ReviewReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        try:
            review = Review.objects.get(id=self.kwargs['review_id'])
            context['review'] = review
        except Review.DoesNotExist:
            pass
        return context

    def create(self, request, *args, **kwargs):
        try:
            review = Review.objects.get(id=kwargs['review_id'])
            
            # Check if user already reported this review
            if ReviewReport.objects.filter(
                review=review,
                reporter=request.user
            ).exists():
                return Response(
                    {'error': 'You have already reported this review'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            return super().create(request, *args, **kwargs)
        except Review.DoesNotExist:
            return Response({'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def product_review_stats(request, product_id):
    """
    Get review statistics for a product.
    """
    try:
        product = Product.objects.get(id=product_id)
        reviews = Review.objects.filter(product=product)
        
        stats = {
            'total_reviews': reviews.count(),
            'average_rating': reviews.aggregate(Avg('rating'))['rating__avg'] or 0,
            'rating_distribution': {},
            'verified_reviews': reviews.filter(is_verified=True).count(),
        }
        
        # Rating distribution
        for i in range(1, 6):
            stats['rating_distribution'][str(i)] = reviews.filter(rating=i).count()
        
        # Detailed ratings averages
        stats['communication_avg'] = reviews.aggregate(
            Avg('communication_rating')
        )['communication_rating__avg'] or 0
        
        stats['delivery_avg'] = reviews.aggregate(
            Avg('delivery_rating')
        )['delivery_rating__avg'] or 0
        
        stats['description_avg'] = reviews.aggregate(
            Avg('item_description_rating')
        )['item_description_rating__avg'] or 0
        
        return Response(stats)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def user_review_stats(request, user_id):
    """
    Get review statistics for a user (seller).
    """
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User.objects.get(id=user_id)
        
        reviews = Review.objects.filter(reviewee=user)
        
        stats = {
            'total_reviews': reviews.count(),
            'average_rating': reviews.aggregate(Avg('rating'))['rating__avg'] or 0,
            'rating_distribution': {},
            'verified_reviews': reviews.filter(is_verified=True).count(),
            'response_rate': 0,
        }
        
        # Rating distribution
        for i in range(1, 6):
            stats['rating_distribution'][str(i)] = reviews.filter(rating=i).count()
        
        # Response rate
        total_reviews = reviews.count()
        if total_reviews > 0:
            responded_reviews = reviews.filter(response__isnull=False).count()
            stats['response_rate'] = (responded_reviews / total_reviews) * 100
        
        return Response(stats)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)