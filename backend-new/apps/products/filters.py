"""
Filters for products.
"""
import django_filters
from django.db.models import Q
from .models import Product
from apps.categories.models import Category


class ProductFilter(django_filters.FilterSet):
    """
    Filter set for products with advanced filtering options.
    """
    # Price range
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    price_range = django_filters.RangeFilter(field_name='price')
    
    # Category filtering
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.filter(is_active=True))
    category_slug = django_filters.CharFilter(field_name='category__slug')
    
    # Condition
    condition = django_filters.ChoiceFilter(choices=Product.CONDITION_CHOICES)
    
    # Location
    location_city = django_filters.CharFilter(field_name='location__city', lookup_expr='icontains')
    location_state = django_filters.CharFilter(field_name='location__state', lookup_expr='icontains')
    
    # Seller
    seller = django_filters.CharFilter(field_name='seller__id')
    verified_seller = django_filters.BooleanFilter(field_name='seller__is_verified')
    
    # Features
    is_boosted = django_filters.BooleanFilter()
    is_featured = django_filters.BooleanFilter()
    pickup_available = django_filters.BooleanFilter()
    delivery_available = django_filters.BooleanFilter()
    
    # Date filters
    created_after = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    
    # Search in multiple fields
    search = django_filters.CharFilter(method='filter_search')
    
    class Meta:
        model = Product
        fields = [
            'condition', 'is_boosted', 'is_featured', 'pickup_available',
            'delivery_available', 'category', 'seller'
        ]

    def filter_search(self, queryset, name, value):
        """
        Search across multiple fields.
        """
        return queryset.filter(
            Q(title__icontains=value) |
            Q(description__icontains=value) |
            Q(brand__icontains=value) |
            Q(model__icontains=value) |
            Q(tags__name__icontains=value)
        ).distinct()