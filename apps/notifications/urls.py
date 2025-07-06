"""
URL configuration for notifications app.
"""
from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.NotificationListView.as_view(), name='notification-list'),
    path('<uuid:pk>/', views.NotificationDetailView.as_view(), name='notification-detail'),
    path('preferences/', views.NotificationPreferenceView.as_view(), name='notification-preferences'),
    path('devices/', views.NotificationDeviceView.as_view(), name='notification-devices'),
    path('mark-all-read/', views.MarkAllReadView.as_view(), name='mark-all-read'),
    path('stats/', views.notification_stats, name='notification-stats'),
    path('clear-read/', views.clear_read_notifications, name='clear-read'),
]