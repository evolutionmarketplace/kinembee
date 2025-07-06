"""
URL configuration for accounts app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'accounts'

urlpatterns = [
    # Authentication
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    
    # Profile
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('preferences/', views.UserPreferencesView.as_view(), name='preferences'),
    path('dashboard/stats/', views.user_dashboard_stats, name='dashboard-stats'),
    
    # Password management
    path('password/change/', views.PasswordChangeView.as_view(), name='password-change'),
    
    # Email verification
    path('verify-email/', views.EmailVerificationView.as_view(), name='verify-email'),
    path('resend-verification/', views.ResendEmailVerificationView.as_view(), name='resend-verification'),
]