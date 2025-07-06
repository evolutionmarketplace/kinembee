"""
Views for user accounts and authentication.
"""
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login, logout
from django.utils import timezone
from django.conf import settings
from .models import User, UserProfile, UserPreferences, EmailVerification, PhoneVerification
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer,
    UserProfileUpdateSerializer, UserPreferencesSerializer, PasswordChangeSerializer,
    EmailVerificationSerializer, PhoneVerificationSerializer
)
from apps.core.utils import generate_verification_token, send_welcome_email, send_verification_email
import logging

logger = logging.getLogger(__name__)


class UserRegistrationView(generics.CreateAPIView):
    """
    User registration endpoint.
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Create user profile and preferences
        UserProfile.objects.create(user=user)
        UserPreferences.objects.create(user=user)
        
        # Send welcome email
        send_welcome_email(user)
        
        # Send verification email
        self.send_verification_email(user)
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserProfileSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            'message': 'Registration successful. Please check your email for verification.'
        }, status=status.HTTP_201_CREATED)

    def send_verification_email(self, user):
        """Send email verification."""
        token = generate_verification_token()
        expires_at = timezone.now() + timezone.timedelta(hours=24)
        
        EmailVerification.objects.create(
            user=user,
            token=token,
            email=user.email,
            expires_at=expires_at
        )
        
        verification_url = f"{settings.FRONTEND_URL}/verify-email/{token}"
        send_verification_email(user, verification_url)


class UserLoginView(APIView):
    """
    User login endpoint.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        
        # Update last login info
        user.last_login = timezone.now()
        user.last_login_ip = self.get_client_ip(request)
        user.save()
        
        # Log activity
        from .models import UserActivity
        UserActivity.objects.create(
            user=user,
            activity_type='login',
            ip_address=self.get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserProfileSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        })

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class UserLogoutView(APIView):
    """
    User logout endpoint.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            # Log activity
            from .models import UserActivity
            UserActivity.objects.create(
                user=request.user,
                activity_type='logout',
                ip_address=self.get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
            
            return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    User profile view and update.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UserProfileUpdateSerializer
        return UserProfileSerializer


class UserPreferencesView(generics.RetrieveUpdateAPIView):
    """
    User preferences view and update.
    """
    serializer_class = UserPreferencesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        preferences, created = UserPreferences.objects.get_or_create(user=self.request.user)
        return preferences


class PasswordChangeView(APIView):
    """
    Password change endpoint.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        # Log activity
        from .models import UserActivity
        UserActivity.objects.create(
            user=request.user,
            activity_type='password_change',
            ip_address=self.get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        return Response({"message": "Password changed successfully"})

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class EmailVerificationView(APIView):
    """
    Email verification endpoint.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = EmailVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        verification = serializer.verification
        user = verification.user
        
        # Mark email as verified
        user.is_verified = True
        user.save()
        
        # Mark verification as used
        verification.is_used = True
        verification.save()
        
        # Update profile
        profile = user.profile
        profile.email_verified = True
        profile.save()
        
        return Response({"message": "Email verified successfully"})


class ResendEmailVerificationView(APIView):
    """
    Resend email verification.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        
        if user.is_verified:
            return Response({"message": "Email already verified"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if there's a recent verification email
        recent_verification = EmailVerification.objects.filter(
            user=user,
            created_at__gte=timezone.now() - timezone.timedelta(minutes=5)
        ).first()
        
        if recent_verification:
            return Response(
                {"message": "Verification email already sent recently. Please wait 5 minutes."},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )
        
        # Send new verification email
        token = generate_verification_token()
        expires_at = timezone.now() + timezone.timedelta(hours=24)
        
        EmailVerification.objects.create(
            user=user,
            token=token,
            email=user.email,
            expires_at=expires_at
        )
        
        verification_url = f"{settings.FRONTEND_URL}/verify-email/{token}"
        send_verification_email(user, verification_url)
        
        return Response({"message": "Verification email sent"})


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_dashboard_stats(request):
    """
    Get user dashboard statistics.
    """
    user = request.user
    
    # Get user's listings count
    from apps.products.models import Product
    active_listings = Product.objects.filter(seller=user, is_active=True).count()
    total_listings = Product.objects.filter(seller=user).count()
    
    # Get user's reviews
    from apps.reviews.models import Review
    reviews_received = Review.objects.filter(product__seller=user).count()
    
    # Get user's messages
    from apps.chat.models import Conversation
    unread_messages = Conversation.objects.filter(
        participants=user,
        messages__is_read=False
    ).exclude(messages__sender=user).distinct().count()
    
    stats = {
        'active_listings': active_listings,
        'total_listings': total_listings,
        'reviews_received': reviews_received,
        'unread_messages': unread_messages,
        'seller_rating': user.profile.seller_rating,
        'total_sales': user.profile.total_sales,
        'verification_level': user.profile.verification_level,
    }
    
    return Response(stats)