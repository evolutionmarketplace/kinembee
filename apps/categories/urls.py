"""
URL configuration for categories app.
"""
from django.urls import path
from . import views

app_name = 'categories'

urlpatterns = [
    path('', views.CategoryListView.as_view(), name='category-list'),
    path('tree/', views.category_tree, name='category-tree'),
    path('featured/', views.featured_categories, name='featured-categories'),
    path('stats/', views.category_stats, name='category-stats'),
    path('<slug:slug>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('<slug:category_slug>/attributes/', views.category_attributes, name='category-attributes'),
]