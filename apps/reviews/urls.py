"""
URL configuration for reviews app.
"""
from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    # Review listing and creation
    path('', views.ReviewListView.as_view(), name='review-list'),
    path('create/', views.ReviewCreateView.as_view(), name='review-create'),
    path('my-reviews/', views.MyReviewsView.as_view(), name='my-reviews'),
    
    # Review details and actions
    path('<uuid:pk>/', views.ReviewDetailView.as_view(), name='review-detail'),
    path('<uuid:review_id>/helpful/', views.ReviewHelpfulView.as_view(), name='review-helpful'),
    path('<uuid:review_id>/respond/', views.ReviewResponseView.as_view(), name='review-respond'),
    path('<uuid:review_id>/report/', views.ReviewReportView.as_view(), name='review-report'),
    
    # Statistics
    path('product/<uuid:product_id>/stats/', views.product_review_stats, name='product-review-stats'),
    path('user/<uuid:user_id>/stats/', views.user_review_stats, name='user-review-stats'),
]