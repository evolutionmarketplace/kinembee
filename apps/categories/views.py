"""
Views for categories.
"""
from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Category, CategoryAttribute, CategoryTag
from .serializers import (
    CategorySerializer, CategoryListSerializer, CategoryTreeSerializer,
    CategoryAttributeSerializer, CategoryTagSerializer
)


class CategoryListView(generics.ListAPIView):
    """
    List all active categories.
    """
    serializer_class = CategoryListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category_type', 'featured', 'parent']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'sort_order', 'product_count']
    ordering = ['sort_order', 'name']

    def get_queryset(self):
        return Category.objects.filter(is_active=True)


class CategoryDetailView(generics.RetrieveAPIView):
    """
    Retrieve a specific category with full details.
    """
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'

    def get_queryset(self):
        return Category.objects.filter(is_active=True)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def category_tree(request):
    """
    Get the complete category tree structure.
    """
    root_categories = Category.objects.filter(
        parent=None,
        is_active=True,
        show_in_menu=True
    ).order_by('sort_order', 'name')
    
    serializer = CategoryTreeSerializer(root_categories, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def featured_categories(request):
    """
    Get featured categories for homepage.
    """
    categories = Category.objects.filter(
        is_active=True,
        featured=True
    ).order_by('sort_order', 'name')[:8]
    
    serializer = CategoryListSerializer(categories, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def category_attributes(request, category_slug):
    """
    Get attributes for a specific category.
    """
    try:
        category = Category.objects.get(slug=category_slug, is_active=True)
        attributes = CategoryAttribute.objects.filter(
            category=category
        ).order_by('sort_order', 'name')
        
        serializer = CategoryAttributeSerializer(attributes, many=True)
        return Response(serializer.data)
    except Category.DoesNotExist:
        return Response({'error': 'Category not found'}, status=404)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def category_stats(request):
    """
    Get category statistics.
    """
    stats = {
        'total_categories': Category.objects.filter(is_active=True).count(),
        'goods_categories': Category.objects.filter(
            is_active=True,
            category_type__in=['goods', 'both']
        ).count(),
        'services_categories': Category.objects.filter(
            is_active=True,
            category_type__in=['services', 'both']
        ).count(),
        'featured_categories': Category.objects.filter(
            is_active=True,
            featured=True
        ).count(),
    }
    
    return Response(stats)