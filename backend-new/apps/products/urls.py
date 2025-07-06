"""
URL configuration for products app.
"""
from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # Product listing and details
    path('', views.ProductListView.as_view(), name='product-list'),
    path('featured/', views.featured_products, name='featured-products'),
    path('trending/', views.trending_products, name='trending-products'),
    path('stats/', views.product_stats, name='product-stats'),
    
    # Product CRUD
    path('create/', views.ProductCreateView.as_view(), name='product-create'),
    path('my-products/', views.MyProductsView.as_view(), name='my-products'),
    path('<uuid:pk>/update/', views.ProductUpdateView.as_view(), name='product-update'),
    path('<uuid:pk>/delete/', views.ProductDeleteView.as_view(), name='product-delete'),
    path('<uuid:product_id>/sold/', views.mark_as_sold, name='mark-as-sold'),
    
    # Product details
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='product-detail'),
    
    # Wishlist
    path('wishlist/', views.ProductWishlistView.as_view(), name='wishlist'),
    path('wishlist/<uuid:product_id>/remove/', views.ProductWishlistRemoveView.as_view(), name='wishlist-remove'),
    
    # Reports
    path('<uuid:product_id>/report/', views.ProductReportView.as_view(), name='product-report'),
    
    # Saved searches
    path('saved-searches/', views.SavedSearchListView.as_view(), name='saved-search-list'),
    path('saved-searches/<uuid:pk>/', views.SavedSearchDetailView.as_view(), name='saved-search-detail'),
]