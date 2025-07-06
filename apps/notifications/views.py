"""
Views for notifications.
"""
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from django.utils import timezone
from .models import Notification, NotificationPreference, NotificationDevice
from .serializers import (
    NotificationSerializer, NotificationPreferenceSerializer,
    NotificationDeviceSerializer
)
from apps.core.pagination import CustomPageNumberPagination


class NotificationListView(generics.ListAPIView):
    """
    List user's notifications.
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        user = self.request.user
        queryset = Notification.objects.filter(recipient=user)
        
        # Filter by read status
        is_read = self.request.query_params.get('is_read')
        if is_read is not None:
            queryset = queryset.filter(is_read=is_read.lower() == 'true')
        
        # Filter by priority
        priority = self.request.query_params.get('priority')
        if priority:
            queryset = queryset.filter(priority=priority)
        
        return queryset.order_by('-created_at')


class NotificationDetailView(generics.RetrieveUpdateAPIView):
    """
    Retrieve and update a specific notification.
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)

    def perform_update(self, serializer):
        # Auto-mark as read when accessed
        if not serializer.instance.is_read:
            serializer.save(is_read=True, read_at=timezone.now())


class NotificationPreferenceView(generics.RetrieveUpdateAPIView):
    """
    Get and update notification preferences.
    """
    serializer_class = NotificationPreferenceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        preferences, created = NotificationPreference.objects.get_or_create(
            user=self.request.user
        )
        return preferences


class NotificationDeviceView(generics.ListCreateAPIView):
    """
    List and register notification devices.
    """
    serializer_class = NotificationDeviceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return NotificationDevice.objects.filter(user=self.request.user)


class MarkAllReadView(APIView):
    """
    Mark all notifications as read.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        count = Notification.objects.filter(
            recipient=request.user,
            is_read=False
        ).update(is_read=True, read_at=timezone.now())
        
        return Response({
            'message': f'{count} notifications marked as read'
        })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def notification_stats(request):
    """
    Get notification statistics for the user.
    """
    user = request.user
    
    stats = {
        'total_notifications': Notification.objects.filter(recipient=user).count(),
        'unread_count': Notification.objects.filter(recipient=user, is_read=False).count(),
        'high_priority_unread': Notification.objects.filter(
            recipient=user, 
            is_read=False, 
            priority='high'
        ).count(),
        'urgent_unread': Notification.objects.filter(
            recipient=user, 
            is_read=False, 
            priority='urgent'
        ).count(),
    }
    
    return Response(stats)


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def clear_read_notifications(request):
    """
    Clear all read notifications.
    """
    count = Notification.objects.filter(
        recipient=request.user,
        is_read=True
    ).delete()[0]
    
    return Response({
        'message': f'{count} read notifications cleared'
    })